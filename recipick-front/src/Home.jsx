import { useState } from "react";
import { Header } from "./components/Header";
import { Hello } from "./components/Hello";
import { ParametersChips } from "./components/ParametersChips";
import { MessageInput } from "./MessageInput";
import { PrimaryButton } from "./components/PrimaryButton";
import { api } from "./api";
import { AIMessage } from "./components/AIMessage";

export function Home() {
  const [ingredients, setIngredients] = useState([]);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  async function handleGenerateRecipes() {
    if (ingredients.length === 0) {
      return;
    }
    try {
      setIsLoading(true);
      // TODO: It don't make sense to make an extra request to normalize ingredients
      // We can just send the ingredients directly to the recipe generation endpoint
      const { data } = await api.post("/normalizar-ingredientes", {
        ingredientes: ingredients,
      });
      const response = await api.post("/receitas", {
        ingredientes: data.ingredientes_normalizados
          .filter((ingredient) => ingredient.trim() !== "")
          .join(", "),
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: response.data.receitas,
        },
      ]);
    } catch (error) {
      console.error("Erro ao normalizar ingredientes:", error);
      alert("Ocorreu um erro ao processar os ingredientes. Tente novamente.");
    } finally {
      setIsLoading(false);
    }
  }

  function handleAddIngredient(newIngredient) {
    if (!newIngredient || newIngredient.trim() === "") {
      return;
    }
    setIngredients((prev) => [...prev, newIngredient]);
  }

  function handleRefineRecipes(message) {
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: message,
      },
    ]);

    console.log("Refinando receitas com a mensagem:", message);
  }

  function handleOnSend(message) {
    if (messages.length === 0) {
      handleAddIngredient(message);
    } else {
      handleRefineRecipes(message);
    }
  }

  return (
    <div className="flex flex-col items-center justify-between bg-bg px-4 h-dvh">
      <Header />
      <main className="flex flex-col items-center h-full mb-6">
        <div className="h-full flex flex-col items-center justify-center">
          <div className="flex flex-col items-center justify-center gap-4">
            <Hello />
            <ParametersChips
              params={ingredients}
              editable={true}
              onRemove={(index) => {
                setIngredients((prev) => prev.filter((_, i) => i !== index));
              }}
            />
          </div>
        </div>
        <div className="flex flex-col items-start justify-center w-full max-w-2xl mt-6">
          {(messages.length > 0 || isLoading) && (
            <div className="flex flex-col items-start justify-center gap-4 mt-6">
              {messages.map((message, index) =>
                message.role == "assistant" ? (
                  <AIMessage key={index} message={message.content} />
                ) : (
                  <div className="flex flex-col items-center justify-center p-2 bg-blue-50 text-black rounded-xl shadow-md text-sm">
                    {message.content}
                  </div>
                )
              )}
              {isLoading && (
                <div className="flex items-center justify-center w-full h-12">
                  <div className="rounded-full h-4 w-4 bg-solid animate-ping"></div>
                </div>
              )}
            </div>
          )}
        </div>
        <div className="flex flex-col items-end justify-center gap-4 w-full mt-6">
          {ingredients.length > 0 && messages.length == 0 && !isLoading && (
            <PrimaryButton onClick={handleGenerateRecipes}>
              Continuar
            </PrimaryButton>
          )}
          <MessageInput
            placeholder={
              messages.length == 0
                ? "Digite um ingrediente ou preferência"
                : "O que você acha?"
            }
            disabled={isLoading}
            onSend={handleOnSend}
          />
        </div>
      </main>
    </div>
  );
}
