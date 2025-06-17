import { useState, useRef, useEffect, useCallback } from "react";
import { Header } from "./components/Header";
import { Hello } from "./components/Hello";
import { ParametersChips } from "./components/ParametersChips";
import { MessageInput } from "./MessageInput";
import { SettingsModal } from "./components/SettingsModal";
import ReactMarkdown from "react-markdown";

const defaultSettings = {
  portionSize: 'medio',
  complexity: 'rapida',
  style: 'criativo',
  isVegetarian: false,
  restrictions: '',
};

function Home() {
  const [ingredientes, setIngredientes] = useState([]);
  const [ingredientesSalvos, setIngredientesSalvos] = useState([]);
  const [resposta, setResposta] = useState("");
  const [resultadoPesquisa, setResultadoPesquisa] = useState(null);
  const [settings, setSettings] = useState(defaultSettings);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isNormalizing, setIsNormalizing] = useState(false);
  const latestRequestRef = useRef(0);

  useEffect(() => {
    try {
      const savedSettings = localStorage.getItem('recipeSettings');
      if (savedSettings) {
        setSettings(JSON.parse(savedSettings));
      }
    } catch (error) {
      console.error("Falha ao carregar configurações do localStorage:", error);
    }
  }, []);
  
  const enviarIngredientes = useCallback(async (lista) => {
    latestRequestRef.current += 1;
    const requestId = latestRequestRef.current;
    
    try {
      const response = await fetch("http://localhost:5000/api/receitas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          ingredientes: lista.join(", "),
          settings: settings
        }),
      });
      const data = await response.json();

      if (requestId === latestRequestRef.current) {
        setResposta(data.receitas);
      }
    } catch (err) {
      console.error("Erro ao buscar sugestões:", err);
    }
  }, [settings]);

  useEffect(() => {
    // Se não estivermos em modo pesquisa (sem ingredientes salvos), busca receitas ao mudar settings
    if (ingredientes.length > 0 && ingredientesSalvos.length === 0) {
      enviarIngredientes(ingredientes);
    }
  }, [settings, ingredientes, ingredientesSalvos, enviarIngredientes]);

  function handleSettingsChange(changedSetting) {
    const newSettings = { ...settings, ...changedSetting };
    setSettings(newSettings);
    localStorage.setItem('recipeSettings', JSON.stringify(newSettings));
  }

  async function adicionarIngredientes(textoInput) {
    setIsNormalizing(true);
    setResultadoPesquisa(null);

    const ingredientesPotenciais = textoInput
      .split(/,|\s+e\s+/)
      .map(ing => ing.trim())
      .filter(ing => ing.length > 0);

    if (ingredientesPotenciais.length === 0) {
        setIsNormalizing(false);
        return;
    };

    try {
      const response = await fetch("http://localhost:5000/api/normalizar-ingredientes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ingredientes: ingredientesPotenciais }),
      });
      const data = await response.json();
      
      const ingredientesValidos = data.ingredientes_normalizados
        .map(ing => ing.toLowerCase())
        .filter(ing => ing && !ingredientes.includes(ing));
      
      const ingredientesUnicos = [...new Set(ingredientesValidos)];

      if (ingredientesUnicos.length > 0) {
        const listaFinalAtualizada = [...ingredientes, ...ingredientesUnicos];
        setIngredientes(listaFinalAtualizada);
        enviarIngredientes(listaFinalAtualizada);
      }

    } catch (error) {
      console.error("Erro ao normalizar ingredientes:", error);
    } finally {
      setIsNormalizing(false);
    }
  }

  function removerIngrediente(index) {
    setResultadoPesquisa(null);
    const novos = [...ingredientes];
    novos.splice(index, 1);
    setIngredientes(novos);

    if (novos.length === 0) {
      latestRequestRef.current += 1;
      setResposta("");
    } else {
      enviarIngredientes(novos);
    }
  }
  
  function entrarModoPesquisa() {
    latestRequestRef.current += 1;
    setIngredientesSalvos(ingredientes);
    setIngredientes([]);
    setResposta("");
    setResultadoPesquisa(null);
  }

  // FUNÇÃO CORRIGIDA
  function sairModoPesquisa() {
    setIngredientes(ingredientesSalvos); // Restaura os balões
    setResposta(""); // 1. Limpa a mensagem "Ok, qual receita..."
    
    // 2. Se existiam ingredientes salvos, busca as receitas para eles
    if (ingredientesSalvos.length > 0) {
      enviarIngredientes(ingredientesSalvos);
    }
    
    setIngredientesSalvos([]); // Limpa a lista de ingredientes salvos
  }

  function limparTudo() {
    latestRequestRef.current += 1;
    setIngredientes([]);
    setResposta("");
    setIngredientesSalvos([]);
    setResultadoPesquisa(null);
  }

  async function buscarReceitaPorNome(nome) {
    try {
      const response = await fetch("http://localhost:5000/api/pesquisar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          nome_receita: nome,
          settings: settings
        }),
      });
      const data = await response.json();
      setResultadoPesquisa(data.receita);
    } catch (err) {
      console.error("Erro ao pesquisar receita:", err);
    }
  }

  const conteudoParaExibir = resultadoPesquisa || resposta;

  return (
    <div className="flex flex-col h-screen w-full items-center px-4 py-8 overflow-hidden">
      {isSettingsOpen && (
        <SettingsModal 
          settings={settings}
          onSettingsChange={handleSettingsChange}
          onClose={() => setIsSettingsOpen(false)} 
        />
      )}

      <Header onSettingsClick={() => setIsSettingsOpen(true)} />
      
      <main className="flex w-full max-w-lg grow flex-col gap-2 overflow-y-auto px-1">
        <Hello name="!" />
        <ParametersChips params={ingredientes} onRemove={removerIngrediente} />
        
        {conteudoParaExibir && (
          <div className="text-sm whitespace-pre-line bg-white rounded-xl shadow p-4 max-h-96 overflow-y-auto">
            <ReactMarkdown>{conteudoParaExibir}</ReactMarkdown>
          </div>
        )}

        <MessageInput
          isNormalizing={isNormalizing}
          onAdicionarIngredientes={adicionarIngredientes}
          onLimparTudo={limparTudo}
          onEntrarModoPesquisa={entrarModoPesquisa}
          onSairModoPesquisa={sairModoPesquisa}
          onBuscarReceita={buscarReceitaPorNome}
          onResposta={setResposta}
        />
      </main>
    </div>
  );
}

export default Home;