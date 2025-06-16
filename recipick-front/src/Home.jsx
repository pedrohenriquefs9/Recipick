
import { useState } from "react";
import { Header } from "./components/Header";
import { Hello } from "./components/Hello";
import { ParametersChips } from "./components/ParametersChips";
import { MessageInput } from "./MessageInput";
import ReactMarkdown from "react-markdown";

function Home() {
  const [ingredientes, setIngredientes] = useState([]);
  const [resposta, setResposta] = useState("");

  function adicionarIngrediente(novo) {
    if (!ingredientes.includes(novo.toLowerCase())) {
      const atualizados = [...ingredientes, novo.toLowerCase()];
      setIngredientes(atualizados);
      enviarIngredientes(atualizados);
    }
  }

  function limparIngredientes() {
    setIngredientes([]);
  }

  function removerIngrediente(index) {
  const novos = [...ingredientes];
  novos.splice(index, 1);
  setIngredientes(novos);

  if (novos.length === 0) {
    setResposta("");
  } else {
    enviarIngredientes(novos);
  }
}

  async function enviarIngredientes(lista) {
    try {
      const response = await fetch("http://localhost:5000/api/receitas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ingredientes: lista.join(", ") }),
      });
      const data = await response.json();
      setResposta(data.receitas);
    } catch (err) {
      console.error("Erro ao buscar sugestões:", err);
    }
  }

  return (
    <div className="flex flex-col h-screen w-full items-center px-4 py-8 overflow-hidden">
      <Header />
      <main className="flex w-full max-w-lg grow flex-col gap-2 overflow-y-auto px-1">
        <Hello />
        <ParametersChips params={ingredientes} onRemove={removerIngrediente} />
        {resposta && (
          <div className="text-sm whitespace-pre-line bg-white rounded-xl shadow p-4 max-h-96 overflow-y-auto">
            <ReactMarkdown>{resposta}</ReactMarkdown>
          </div>
        )}
        <MessageInput
          ingredientes={ingredientes}
          onAdicionarIngrediente={adicionarIngrediente}
          onResposta={setResposta}
          onLimpar={limparIngredientes}
        />
      </main>
    </div>
  );
}

export default Home;
