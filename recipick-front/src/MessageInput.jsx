
import { useState } from "react";
import { PlusIcon } from "@heroicons/react/16/solid";
import { CameraIcon } from "@heroicons/react/24/outline";

// Remoção de acentos e padronização
function normalizarTexto(texto) {
  return texto
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .trim();
}

// Cálculo simples de similaridade (mínimo de igualdade entre strings)
function similaridade(a, b) {
  const minLength = Math.min(a.length, b.length);
  let iguais = 0;
  for (let i = 0; i < minLength; i++) {
    if (a[i] === b[i]) iguais++;
  }
  return iguais / Math.max(a.length, b.length);
}

export function MessageInput({ onAdicionarIngrediente, onResposta, onLimpar, ingredientes }) {
  const [mensagem, setMensagem] = useState("");
  const [modoPesquisa, setModoPesquisa] = useState(false);

  async function buscarReceitaPorNome(nome) {
    try {
      const response = await fetch("http://localhost:5000/api/pesquisar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome_receita: nome }),
      });
      const data = await response.json();
      onResposta(data.receita);
    } catch (err) {
      console.error("Erro ao pesquisar receita:", err);
    }
  }

  function handleSubmit(event) {
    event.preventDefault();
    const input = mensagem.trim();
    if (!input) return;

    const normalizado = normalizarTexto(input);

    const duplicado = ingredientes.some((ing) => {
      const ingNormalizado = normalizarTexto(ing);
      return (
        ingNormalizado === normalizado ||
        similaridade(ingNormalizado, normalizado) > 0.8
      );
    });

    if (duplicado) {
      setMensagem("");
      return;
    }

    if (input.toLowerCase().includes("pesquisar receita")) {
      setModoPesquisa(true);
      onResposta("Digite o nome da receita que deseja buscar:");
    } else if (modoPesquisa) {
      buscarReceitaPorNome(input);
      setModoPesquisa(false);
      onLimpar();
    } else {
      onAdicionarIngrediente(input);
    }

    setMensagem("");
  }

  return (
    <div className="flex flex-col items-center justify-center gap-2 w-full">
      <form
        onSubmit={handleSubmit}
        className="flex items-center justify-between gap-2 w-full"
      >
        <button
          type="button"
          className="flex flex-shrink-0 cursor-pointer items-center justify-center rounded-full bg-solid p-1 h-12 w-12"
        >
          <CameraIcon className="text-black w-7 h-7" />
        </button>
        <div className="flex justify-between items-center w-full gap-1 text-black bg-solid rounded-full px-3 py-2">
          <input
            type="text"
            name="message"
            id="message"
            value={mensagem}
            onChange={(e) => setMensagem(e.target.value)}
            className="outline-0 w-full text-sm"
            placeholder="Digite um ingrediente ou 'pesquisar receita'"
          />
          <button
            type="submit"
            className="cursor-pointer rounded-full bg-solid-dark p-1"
          >
            <PlusIcon className="h-6 w-6 text-dark-light" />
          </button>
        </div>
      </form>
      <small className="text-[10px] text-center text-dark-light">
        O ReciPick pode cometer erros. Verifique as informações.
      </small>
    </div>
  );
}
