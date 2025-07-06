import { useAppState } from "./store/AppContext";
import { Header } from "./components/Header";
import { Hello } from "./components/Hello";
import { ParametersChips } from "./components/ParametersChips";
import { MessageInput } from "./MessageInput";
import { PrimaryButton } from "./components/PrimaryButton";
import { api } from "./api";
import { AIMessage } from "./components/AIMessage";

export function Home() {
  // Use o estado e o dispatch do nosso contexto global
  const { state, dispatch } = useAppState();
  const { ingredients, messages, isLoading } = state;

  async function handleGenerateRecipes() {
    if (ingredients.length === 0) {
      return;
    }
    try {
      dispatch({ type: "START_LOADING" });

      const { data } = await api.post("/normalizar-ingredientes", {
        ingredientes: ingredients,
      });

      const response = await api.post("/receitas", {
        ingredientes: data.ingredientes_normalizados
          .filter((ingredient) => ingredient.trim() !== "")
          .join(", "),
        settings: state.settings, // Enviando as configurações para o backend
      });

      // Adiciona a resposta da IA às mensagens
      dispatch({
        type: "ADD_MESSAGE",
        payload: {
          role: "assistant",
          content: response.data.receitas,
        },
      });
    } catch (error) {
      console.error("Erro ao gerar receitas:", error);
      dispatch({
        type: "SET_ERROR",
        payload: "Ocorreu um erro ao processar sua solicitação. Tente novamente.",
      });
      dispatch({
        type: "ADD_MESSAGE",
        payload: {
          role: "assistant",
          content: "Desculpe, não consegui gerar as receitas. Por favor, tente novamente.",
        },
      });
    }
  }

  function handleAddIngredient(newIngredient) {
    if (!newIngredient || newIngredient.trim() === "") {
      return;
    }
    dispatch({ type: "ADD_INGREDIENT", payload: newIngredient });
  }
  
  function handleRemoveIngredient(index) {
    dispatch({ type: "REMOVE_INGREDIENT", payload: index });
  }

  function handleRefineRecipes(message) {
     dispatch({
        type: "ADD_MESSAGE",
        payload: {
          role: "user",
          content: message,
        },
      });
    // Aqui viria a lógica para refinar, que pode ser uma nova chamada de API
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
              onRemove={handleRemoveIngredient}
            />
          </div>
        </div>
        <div className="flex flex-col items-start justify-center w-full max-w-2xl mt-6">
          {(messages.length > 0 || isLoading) && (
            <div className="flex flex-col items-start justify-center gap-4 mt-6">
              {messages.map((message, index) =>
                message.role === "assistant" ? (
                  <AIMessage key={index} message={message.content} />
                ) : (
                  <div key={index} className="flex flex-col items-center justify-center p-2 bg-blue-50 text-black rounded-xl shadow-md text-sm self-end">
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
          {ingredients.length > 0 && messages.length === 0 && !isLoading && (
            <PrimaryButton onClick={handleGenerateRecipes}>
              Continuar
            </PrimaryButton>
          )}
          <MessageInput
            placeholder={
              messages.length === 0
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