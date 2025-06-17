import { useState, useEffect } from "react";
import { PlusIcon } from "@heroicons/react/16/solid";
import { CameraIcon, ArrowPathIcon } from "@heroicons/react/24/outline";
import clsx from "clsx";

const comandos = ["/pesquisar", "/clear"];

export function MessageInput({ isNormalizing, onAdicionarIngredientes, onLimparTudo, onEntrarModoPesquisa, onSairModoPesquisa, onBuscarReceita, onResposta }) {
  const [mensagem, setMensagem] = useState("");
  const [modoPesquisa, setModoPesquisa] = useState(false);
  const [sugestoes, setSugestoes] = useState([]);
  const [sugestaoAtivaIndex, setSugestaoAtivaIndex] = useState(0);

  useEffect(() => {
    if (sugestoes.length > 0) {
      setSugestaoAtivaIndex(0);
    }
  }, [sugestoes]);

  const handleInputChange = (e) => {
    const valor = e.target.value;
    setMensagem(valor);

    if (valor.startsWith("/")) {
      const sugestoesFiltradas = comandos.filter(comando => 
        comando.startsWith(valor.toLowerCase())
      );
      setSugestoes(sugestoesFiltradas);
    } else {
      setSugestoes([]);
    }
  };
  
  const handleSugestaoClick = (sugestao) => {
    setMensagem(sugestao);
    setSugestoes([]);
  };

  const handleKeyDown = (e) => {
    if (sugestoes.length === 0) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSugestaoAtivaIndex((prevIndex) => (prevIndex + 1) % sugestoes.length);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSugestaoAtivaIndex((prevIndex) => (prevIndex - 1 + sugestoes.length) % sugestoes.length);
    } 
    else if (e.key === "Tab" || e.key === "Enter") {
      e.preventDefault();
      handleSugestaoClick(sugestoes[sugestaoAtivaIndex]);
    }
  };

  function handleSubmit(event) {
    event.preventDefault();
    const input = mensagem.trim();
    
    if (sugestoes.length > 0 && (event.nativeEvent.submitter === null || event.key === 'Enter')) {
        handleSugestaoClick(sugestoes[sugestaoAtivaIndex]);
        return;
    }

    setSugestoes([]);

    if (input.toLowerCase() === "/clear") {
      if (modoPesquisa) {
        onSairModoPesquisa();
        setModoPesquisa(false);
      } else {
        onLimparTudo();
      }
      setMensagem("");
      return;
    }
    
    if (input.toLowerCase() === "/pesquisar") {
      onEntrarModoPesquisa();
      setModoPesquisa(true);
      onResposta("Ok, qual receita você quer pesquisar?");
      setMensagem("");
      return;
    }
    
    if (!input) return;

    if (modoPesquisa) {
      onBuscarReceita(input);
      onSairModoPesquisa();
      setModoPesquisa(false);
    } else {
      onAdicionarIngredientes(input);
    }

    setMensagem("");
  }

  const placeholderText = modoPesquisa 
    ? "Digite a receita para pesquisar" 
    : "Coloque seus ingredientes";

  return (
    <div className="relative flex flex-col items-center justify-center gap-2 w-full">
      {sugestoes.length > 0 && (
        <div className="absolute bottom-full mb-2 w-full bg-white border border-solid-dark rounded-lg shadow-lg z-10 overflow-hidden">
          {sugestoes.map((sugestao, index) => (
            <div
              key={index}
              className={clsx(
                "p-2 cursor-pointer text-sm",
                { "bg-bg": index === sugestaoAtivaIndex },
                { "hover:bg-bg": index !== sugestaoAtivaIndex }
              )}
              onClick={() => handleSugestaoClick(sugestao)}
            >
              {sugestao}
            </div>
          ))}
        </div>
      )}

      <form
        onSubmit={handleSubmit}
        className="flex items-center justify-between gap-2 w-full"
      >
        <button
          type="button"
          className="flex flex-shrink-0 cursor-pointer items-center justify-center rounded-full bg-solid p-1 h-12 w-12 hover:bg-solid-dark transition-colors duration-200"
        >
          <CameraIcon className="text-black w-7 h-7" />
        </button>
        
        <div className="relative w-full">
          <div className="flex justify-between items-center w-full gap-1 text-black bg-solid rounded-full px-3 py-2">
            <input
              type="text"
              name="message"
              id="message"
              value={mensagem}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              autoComplete="off"
              disabled={isNormalizing}
              className="outline-0 w-full text-sm bg-transparent disabled:opacity-50"
              placeholder={placeholderText}
            />
            <button
              type="submit"
              disabled={isNormalizing}
              className="cursor-pointer rounded-full bg-solid-dark p-1 group hover:bg-primary-dark transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isNormalizing ? (
                <ArrowPathIcon className="h-6 w-6 text-dark-light animate-spin" />
              ) : (
                <PlusIcon className="h-6 w-6 text-dark-light group-hover:text-white transition-colors duration-200" />
              )}
            </button>
          </div>
        </div>
      </form>
      <small className="text-[10px] text-center text-dark-light">
        O ReciPick pode cometer erros. Verifique as informações.
      </small>
    </div>
  );
}