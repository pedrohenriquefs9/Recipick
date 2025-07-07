import re
from flask import Blueprint
from pytz import timezone
from sqlalchemy import func
from backend.core.database import db
from backend.core.models import ApiCall

history_bp = Blueprint("history", __name__)

def _extract_summary_from_prompt(prompt, endpoint):
    """Função auxiliar para extrair um resumo do prompt."""
    try:
        if endpoint == "/api/receitas":
            match = re.search(r"Com base nos ingredientes: (.*?)\.", prompt, re.DOTALL)
            if match: return f"Ingredientes: {match.group(1).strip()}"
        elif endpoint == "/api/normalizar-ingredientes":
            match = re.search(r"Lista de ingredientes para normalizar: (\[.*?\])", prompt, re.DOTALL)
            if match: return f"Verificando: {match.group(1).strip()}"
        elif endpoint == "/api/pesquisar":
            match = re.search(r"Quero a receita de: (.*?)\.", prompt, re.DOTALL)
            if match: return f"Busca: {match.group(1).strip()}"
        elif endpoint == "/api/refinar-receitas":
            user_inputs = re.findall(r'\*\*User:\*\* (.*?)(?=\n\*\*|$)', prompt, re.DOTALL)
            if user_inputs:
                return f"Usuário: {user_inputs[-1].strip()}"
    except Exception:
        return ""
    return ""

@history_bp.route("/api/history", methods=["GET"])
def get_history():
    try:
        # Lógica para criar um número de "conversa" unificado
        all_calls_asc = ApiCall.query.order_by(ApiCall.timestamp.asc()).all()
        call_id_to_number = {}
        conversation_number = 0
        for call in all_calls_asc:
            # Uma nova conversa começa com a normalização de ingredientes
            if call.endpoint == "/api/normalizar-ingredientes":
                conversation_number += 1
            call_id_to_number[call.id] = conversation_number

        # Busca as chamadas para exibição, da mais nova para a mais antiga
        calls_for_display = ApiCall.query.order_by(ApiCall.timestamp.desc()).all()

        endpoint_map = {
            "/api/receitas": "Geração de Receitas",
            "/api/pesquisar": "Busca por Receita",
            "/api/normalizar-ingredientes": "Correção de Ingredientes",
            "/api/refinar-receitas": "Refinamento de Receita"
        }

        utc_tz = timezone('UTC')
        br_tz = timezone('America/Sao_Paulo')

        html = """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Histórico - ReciPick API</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; background-color: #f4f1ee; color: #222221; margin: 0; padding: 20px; }
                .container { max-width: 900px; margin: 20px auto; background-color: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #8F5008; text-align: center; border-bottom: 2px solid #D4760B; padding-bottom: 10px;}
                .history-item { border: 1px solid #D3CEC9; border-radius: 8px; margin-bottom: 20px; overflow: hidden; }
                .summary { background-color: #f9f9f9; padding: 15px; cursor: pointer; }
                .summary:hover { background-color: #f0f0f0; }
                .summary-header { display: flex; justify-content: space-between; align-items: center; }
                .endpoint { font-weight: bold; font-size: 1.1em; color: #D4760B; }
                .endpoint-counter { font-size: 1.1em; font-weight: normal; color: #8F5008; }
                .timestamp { font-size: 0.9em; color: #565453; flex-shrink: 0; margin-left: 15px; }
                .prompt-summary { font-size: 0.9em; color: #555; margin-top: 5px; font-style: italic; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
                .details { padding: 20px; border-top: 1px solid #D3CEC9; display: none; }
                details[open] .details { display: block; }
                h3 { margin-top: 0; color: #8F5008; border-bottom: 1px solid #eee; padding-bottom: 5px; }
                pre { background-color: #222221; color: #FFFAFA; padding: 15px; border-radius: 5px; white-space: pre-wrap; word-wrap: break-word; font-size: 0.9em; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Histórico de Requisições</h1>
        """

        if not calls_for_display:
            html += "<p style='text-align:center;'>Nenhum registro encontrado.</p>"
        
        for call in calls_for_display:
            # Pega o número da conversa unificado que calculamos
            number = call_id_to_number.get(call.id, 0)

            aware_utc_time = utc_tz.localize(call.timestamp)
            br_time = aware_utc_time.astimezone(br_tz)
            formatted_time = br_time.strftime('%d/%m/%Y às %H:%M:%S')

            friendly_endpoint = endpoint_map.get(call.endpoint, call.endpoint)
            prompt_summary = _extract_summary_from_prompt(call.prompt, call.endpoint)

            html += f"""
            <details class="history-item">
                <summary class="summary">
                    <div class="summary-header">
                        <span class="endpoint">{friendly_endpoint} <span class="endpoint-counter">#{number}</span></span>
                        <span class="timestamp">{formatted_time}</span>
                    </div>
                    <div class="prompt-summary">{prompt_summary}</div>
                </summary>
                <div class="details">
                    <h3>Requisição (Prompt Enviado)</h3>
                    <pre>{call.prompt}</pre>
                    <h3>Resposta da API</h3>
                    <pre>{call.response_text}</pre>
                </div>
            </details>
            """

        html += """
            </div>
        </body>
        </html>
        """
        return html

    except Exception as e:
        return f"<h1>Erro ao acessar o histórico</h1><p>{str(e)}</p>", 500