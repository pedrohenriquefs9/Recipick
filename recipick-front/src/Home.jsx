import { useState, useEffect, useRef } from "react";
import { Header } from "./components/Header";
import { Hello } from "./components/Hello";
import { ParametersChips } from "./components/ParametersChips";
import { MessageInput } from "./MessageInput";
import { PrimaryButton } from "./components/PrimaryButton";
import { api } from "./api";
import { AIMessage } from "./components/AIMessage";
import { RecipeCarousel } from "./components/RecipeCarousel";
import { RecipeDetail } from "./components/RecipeDetail";
import { SettingsModal } from "./components/SettingsModal.jsx"; // Adicionado

const parseApiResponse = (responseData) => {
  if (typeof responseData === 'object' && responseData !== null) {
    return responseData;
  }
  if (typeof responseData === 'string') {
    try {
      return JSON.parse(responseData);
    } catch (e) {
      return { texto: responseData };
    }
  }
  return { texto: "Resposta em formato inesperado." };
};

export function Home() {
  const [ingredients, setIngredients] = useState([]);
  const [messages, setMessages] = useState([]);
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [canGenerate, setCanGenerate] = useState(false);
  const mainContainerRef = useRef(null);

  // --- ADIÇÃO: Lógica para as configurações ---
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [settings, setSettings] = useState({
    diet: 'omnivore',
    complexity: 'rapida',
    style: 'popular',
    portionSize: 'pequeno',
  });
  // ------------------------------------------

  useEffect(() => {
    if (mainContainerRef.current) {
      const { scrollHeight } = mainContainerRef.current;
      mainContainerRef.current.scrollTo({
        top: scrollHeight,
        behavior: 'smooth',
      });
    }
  }, [messages, isLoading]);

  function handleAddIngredient(newIngredient) {
    if (!newIngredient || newIngredient.trim() === "") return;
    const updatedIngredients = [...new Set([...ingredients, newIngredient.trim()])];
    setIngredients(updatedIngredients);
    if (messages.length === 0) {
      setCanGenerate(true);
    }
  }
  
  function handleRemoveIngredient(indexToRemove) {
    const newIngredients = ingredients.filter((_, index) => index !== indexToRemove);
    setIngredients(newIngredients);
    if (newIngredients.length > 0) {
      setCanGenerate(true); 
    } else {
      setCanGenerate(false);
    }
  }

  async function handleGenerateRecipes() {
    if (ingredients.length === 0) return;
    setIsLoading(true);
    setCanGenerate(false); 
    
    const isFirstGeneration = messages.length === 0;
    const userMessageContent = ingredients.join(", ");
    
    const updateUserMessages = (prev) => {
        if (isFirstGeneration) return [{ role: "user", content: userMessageContent, type: 'text' }];
        return [...prev, { role: "user", content: `Ok, gere novas receitas com: ${userMessageContent}`, type: 'text' }];
    };
    setMessages(updateUserMessages);

    try {
      const { data: normalizedData } = await api.post("/normalizar-ingredientes", {
        ingredientes: ingredients,
      });
      
      // ALTERAÇÃO: Envia as configurações para o backend
      const response = await api.post("/receitas", {
        ingredientes: normalizedData.ingredientes_normalizados.filter((i) => i.trim() !== "").join(", "),
        settings: settings,
      });
      
      const data = parseApiResponse(response.data);

      if (data && Array.isArray(data.receitas)) {
        setMessages(prev => [...prev, { role: "assistant", content: data.receitas, type: 'recipe-carousel' }]);
      } else {
         throw new Error("Resposta da API não continha uma lista de receitas.");
      }
    } catch (error) {
      console.error("Erro ao gerar receitas:", error);
      setMessages(prev => [...prev, { role: 'assistant', content: 'Desculpe, não consegui gerar as receitas. Tente novamente.', type: 'text' }]);
    } finally {
      setIsLoading(false);
    }
  }

  async function handleRefineRecipes(messageText) {
    const userMessage = { role: "user", content: messageText, type: 'text' };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await api.post("/refinar-receitas", { 
        historico: [...messages, userMessage],
        ingredientes: ingredients 
      });
      
      const data = parseApiResponse(response.data);
      let newMessages = [];

      if (data && Array.isArray(data.ingredientes_atualizados)) {
        setIngredients(data.ingredientes_atualizados);
        if(!data.receitas) setCanGenerate(true);
      }
      
      if (data && typeof data.texto === 'string') newMessages.push({ role: 'assistant', content: data.texto, type: 'text' });
      if (data && Array.isArray(data.receitas)) {
        setCanGenerate(false);
        newMessages.push({ role: 'assistant', content: data.receitas, type: 'recipe-carousel' });
      }
      
      if (newMessages.length > 0) {
        setMessages(prev => [...prev, ...newMessages]);
      } else if (!data || Object.keys(data).length === 0) {
        throw new Error("Resposta do refinamento vazia ou em formato inesperado.");
      }
    } catch (error) {
      console.error("Erro ao refinar receitas:", error);
      setMessages(prev => [...prev, { role: 'assistant', content: 'Ops, algo deu errado. Tente novamente.', type: 'text' }]);
    } finally {
      setIsLoading(false);
    }
  }

  function handleOnSend(message) {
    if (messages.length === 0) handleAddIngredient(message);
    else handleRefineRecipes(message);
  }
  
  return (
    <div className="flex flex-col items-center justify-between bg-bg px-4 h-dvh">
      <SettingsModal 
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        settings={settings}
        onSettingChange={setSettings}
      />
      <RecipeDetail recipe={selectedRecipe} onClose={() => setSelectedRecipe(null)} />
      <Header onSettingsClick={() => setIsSettingsOpen(true)} />
      
      {ingredients.length > 0 && messages.length > 0 && (
        <div className="w-full max-w-2xl mt-4">
          <ParametersChips params={ingredients} editable={true} onRemove={handleRemoveIngredient} />
        </div>
      )}

      <main ref={mainContainerRef} className="flex flex-col items-center w-full h-full my-4 overflow-y-auto">
        {messages.length === 0 && !isLoading ? (
          <div className="flex flex-col items-center justify-center text-center h-full">
            <div className="flex flex-col items-center justify-center gap-4">
              <Hello />
              {ingredients.length > 0 && (
                <div className="w-full max-w-md pt-4">
                  <ParametersChips params={ingredients} editable={true} onRemove={handleRemoveIngredient} />
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-start w-full max-w-2xl mt-6 space-y-4">
            {messages.map((message, index) => {
              if (message.role === 'user') {
                return <div key={index} className="self-end p-3 bg-primary text-light rounded-xl shadow-md text-sm max-w-lg">{message.content}</div>;
              }
              if (message.role === 'assistant') {
                if (message.type === 'recipe-carousel') return <RecipeCarousel key={index} recipes={message.content} onSelectRecipe={setSelectedRecipe} />;
                return <AIMessage key={index} message={message.content} />;
              }
              return null;
            })}
            {isLoading && (
              <div className="flex items-center justify-start">
                <div className="flex items-center justify-center w-12 h-12">
                  <div className="rounded-full h-4 w-4 bg-solid animate-ping"></div>
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      <div className="w-full max-w-2xl mb-2">
        <div className="flex flex-col items-end justify-center gap-4 w-full mt-auto">
          {canGenerate && (
            <PrimaryButton onClick={handleGenerateRecipes} disabled={isLoading}>
              Continuar
            </PrimaryButton>
          )}
          <MessageInput placeholder={messages.length === 0 ? "Digite um ingrediente..." : "Peça uma alteração ou faça uma pergunta..."} disabled={isLoading} onSend={handleOnSend} />
        </div>
      </div>
    </div>
  );
}