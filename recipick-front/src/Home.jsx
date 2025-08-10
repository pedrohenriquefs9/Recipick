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
import { SettingsModal } from "./components/SettingsModal";
import { Sidebar } from "./components/Sidebar";
import { useAuth } from "./auth/AuthContext";

const createNewChat = () => ({
  id: `local-${Date.now()}`,
  ingredients: [],
  messages: [],
  settings: {
    diet: 'omnivore',
    complexity: 'rapida',
    style: 'popular',
    portionSize: 'pequeno',
  },
  isFavorite: false,
  title: 'Novo Pedido'
});

export function Home() {
  const [chats, setChats] = useState([]);
  const [activeChatId, setActiveChatId] = useState(null);
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [loadingChatIds, setLoadingChatIds] = useState([]);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const mainContainerRef = useRef(null);
  const [canRegenerate, setCanRegenerate] = useState(false);
  const [editingChatId, setEditingChatId] = useState(null);
  const [renamingChatId, setRenamingChatId] = useState(null);
  const { user, logout } = useAuth();

  const activeChat = chats.find(c => c.id === activeChatId);
  const chatToEdit = chats.find(c => c.id === editingChatId);
  const isCurrentChatLoading = activeChatId ? loadingChatIds.includes(activeChatId) : false;

  useEffect(() => {
    const lastMessage = activeChat?.messages[activeChat.messages.length - 1];
    if (lastMessage?.type === 'recipe-carousel') {
      const recipes = lastMessage.content;
      if (!Array.isArray(recipes)) {
        console.error("Conteúdo da mensagem de receitas não é um array:", recipes);
        return;
      }
      recipes.forEach((recipe, index) => {
        if (!recipe.imagemUrl && recipe.titulo) {
          api.post('/buscar-imagem', { titulo: recipe.titulo })
            .then(response => {
              const imageUrl = response.data.imageUrl;
              setChats(currentChats => currentChats.map(chat => {
                if (chat.id === activeChatId) {
                  const newMessages = chat.messages.map((msg, msgIndex) => {
                    if (msgIndex === chat.messages.length - 1) {
                      const updatedRecipes = [...msg.content];
                      updatedRecipes[index].imagemUrl = imageUrl;
                      const updatedMessage = { ...msg, content: updatedRecipes };
                      if (msg.id && !msg.id.toString().startsWith('local-')) {
                        api.put(`/messages/${msg.id}`, { content: JSON.stringify(updatedRecipes) })
                          .catch(err => console.error("Falha ao salvar URL no DB:", err));
                      }
                      return updatedMessage;
                    }
                    return msg;
                  });
                  return { ...chat, messages: newMessages };
                }
                return chat;
              }));
            })
            .catch(err => console.error(`Erro ao buscar imagem para "${recipe.titulo}":`, err));
        }
      });
    }
  }, [activeChat?.messages, activeChatId]);

  useEffect(() => {
    const fetchChats = async () => {
      try {
        const response = await api.get('/chats');
        if (response.data && response.data.length > 0) {
          const parsedChats = response.data.map(chat => {
            const firstUserMessage = chat.messages.find(msg => msg.role === 'user');
            return {
              ...chat,
              ingredients: firstUserMessage ? firstUserMessage.content.split(', ') : [],
              messages: chat.messages.map(msg => {
                if (msg.type === 'recipe-carousel' && typeof msg.content === 'string') {
                  try {
                    return { ...msg, content: JSON.parse(msg.content) };
                  } catch (e) {
                    return { ...msg, content: [] };
                  }
                }
                return msg;
              })
            };
          });
          setChats(parsedChats);
          setActiveChatId(parsedChats[0].id);
        } else {
          const newChat = createNewChat();
          setChats([newChat]);
          setActiveChatId(newChat.id);
        }
      } catch (error) {
        console.error("Erro ao buscar histórico de chats:", error);
        const newChat = createNewChat();
        setChats([newChat]);
        setActiveChatId(newChat.id);
      }
    };
    fetchChats();
  }, []);

  const updateActiveChat = (updater) => {
    setChats(prevChats =>
      prevChats.map(chat =>
        chat.id === activeChatId ? { ...chat, ...updater(chat) } : chat
      )
    );
  };

  useEffect(() => {
    if (mainContainerRef.current) {
      const { scrollHeight } = mainContainerRef.current;
      mainContainerRef.current.scrollTo({
        top: scrollHeight,
        behavior: 'smooth',
      });
    }
  }, [activeChat?.messages, isCurrentChatLoading]);

  function handleAddIngredient(newIngredient) {
    if (!newIngredient || newIngredient.trim() === "") return;
    updateActiveChat(chat => ({
      ingredients: [...new Set([...chat.ingredients, newIngredient.trim()])]
    }));
    setCanRegenerate(false);
  }

  function handleRemoveIngredient(indexToRemove) {
    updateActiveChat(chat => ({
      ingredients: chat.ingredients.filter((_, index) => index !== indexToRemove)
    }));
    if (activeChat && activeChat.messages.length > 0) {
      setCanRegenerate(true);
    }
  }
  
  const handleSettingsChange = async (newSettings) => {
    if (!editingChatId) return;
    setChats(prevChats => prevChats.map(chat =>
        chat.id === editingChatId ? { ...chat, settings: newSettings } : chat
    ));
    if (!editingChatId.toString().startsWith('local-')) {
      try {
        await api.put(`/chats/${editingChatId}`, { settings: newSettings });
      } catch (error) {
        console.error("Erro ao salvar configurações:", error);
      }
    }
  };

  async function handleGenerateRecipes() {
    if (!activeChat || isCurrentChatLoading || activeChat.ingredients.length === 0) return;
    
    const currentChatId = activeChat.id;
    setLoadingChatIds(prev => [...prev, currentChatId]);
    setCanRegenerate(false);

    const userMessageContent = activeChat.ingredients.join(", ");
    const userMessage = { role: "user", content: userMessageContent, type: 'text' };
    
    updateActiveChat(chat => ({ messages: [...chat.messages, userMessage] }));

    try {
      const { data: normalizedData } = await api.post("/normalizar-ingredientes", {
        ingredientes: userMessageContent.split(', '),
      });
      const response = await api.post("/receitas", {
        chatId: currentChatId,
        ingredientes: normalizedData.ingredientes_normalizados.filter((i) => i.trim() !== "").join(", "),
        settings: activeChat.settings,
        userMessage: userMessage,
      });
      const data = response.data;
      
      const recipes = JSON.parse(data.assistantMessage.content);
      const newAssistantMessage = {
          id: data.assistantMessage.id,
          role: 'assistant', 
          content: recipes, 
          type: 'recipe-carousel'
      };

      let finalChatId = data.chatId;
      setChats(prevChats => prevChats.map(chat => {
          if (chat.id === currentChatId) {
              const currentMessages = chat.messages.filter(m => m.role !== 'user' || m.content !== userMessageContent);
              return { ...chat, id: finalChatId, title: data.chatTitle, messages: [...currentMessages, newAssistantMessage] };
          }
          return chat;
      }));
      
      if (activeChatId === currentChatId) {
        setActiveChatId(finalChatId);
      }
    } catch (error) {
      console.error("Erro ao gerar receitas:", error);
      setChats(prevChats => prevChats.map(chat => {
        if (chat.id === currentChatId) {
          return { ...chat, messages: [...chat.messages.slice(0, -1), { role: 'assistant', content: 'Desculpe, não consegui gerar as receitas. Tente novamente.', type: 'text' }] };
        }
        return chat;
      }));
    } finally {
      setLoadingChatIds(prev => prev.filter(id => id !== currentChatId && id !== (activeChat?.id || currentChatId)));
    }
  }
  
  async function handleRefineRecipes(messageText) {
    if (!activeChat || isCurrentChatLoading || activeChat.id.toString().startsWith('local-')) return;
    
    const currentChatId = activeChat.id;
    setCanRegenerate(false);
    setLoadingChatIds(prev => [...prev, currentChatId]);

    const userMessage = { role: "user", content: messageText, type: 'text' };
    updateActiveChat(chat => ({ messages: [...chat.messages, userMessage] }));

    try {
      const response = await api.post("/refinar-receitas", { 
        chatId: currentChatId, historico: [...activeChat.messages, userMessage], ingredientes: activeChat.ingredients, userMessage: userMessage
      });
      const data = response.data;
      let newMessages = [];
      let updatedIngredients = activeChat.ingredients;
      if (data && Array.isArray(data.ingredientes_atualizados)) {
        updatedIngredients = data.ingredientes_atualizados;
      }
      if (data && typeof data.texto === 'string') {
        newMessages.push({ role: 'assistant', content: data.texto, type: 'text', id: data.assistantMessage?.id });
      }
      if (data && Array.isArray(data.receitas)) {
        newMessages.push({ role: 'assistant', content: data.receitas, type: 'recipe-carousel', id: data.assistantMessage?.id });
      }
      setChats(prev => prev.map(chat => {
        if (chat.id === currentChatId) {
          return { ...chat, ingredients: updatedIngredients, messages: [...chat.messages, ...newMessages] };
        }
        return chat;
      }));
    } catch (error) {
      console.error("Erro ao refinar receitas:", error);
      updateActiveChat(chat => ({
        messages: [...chat.messages.slice(0, -1), { role: 'assistant', content: 'Ops, algo deu errado. Não consegui processar sua mensagem.', type: 'text' }]
      }));
    } finally {
      setLoadingChatIds(prev => prev.filter(id => id !== currentChatId));
    }
  }

  function handleOnSend(message) {
    if (!activeChat || isCurrentChatLoading) return;
    const isChatStarted = activeChat.messages.length > 0;
    if (isChatStarted) { handleRefineRecipes(message); } 
    else { handleAddIngredient(message); }
  }

  const handleNewChat = () => {
    setCanRegenerate(false);
    const newChat = createNewChat();
    setChats(prev => [newChat, ...prev]);
    setActiveChatId(newChat.id);
    setIsSidebarOpen(true);
  };

  const handleSelectChat = (id) => {
    setCanRegenerate(false);
    setActiveChatId(id);
  };

  const handleFavoriteChat = async (id) => {
    const chatToUpdate = chats.find(c => c.id === id);
    if (!chatToUpdate || chatToUpdate.id.toString().startsWith('local-')) return;
    const newFavoriteState = !chatToUpdate.isFavorite;
    setChats(prev => prev.map(chat => chat.id === id ? { ...chat, isFavorite: newFavoriteState } : chat));
    try {
      await api.put(`/chats/${id}`, { is_favorite: newFavoriteState });
    } catch (error) {
      console.error("Erro ao favoritar chat:", error);
      setChats(prev => prev.map(chat => chat.id === id ? { ...chat, isFavorite: !newFavoriteState } : chat));
    }
  };

  const handleRemoveChat = async (id) => {
    const chatToRemove = chats.find(c => c.id === id);
    if (!chatToRemove) return;
    if (!window.confirm(`Tem certeza de que deseja remover o chat "${chatToRemove.title}"?`)) return;
    const originalChats = [...chats];
    const newChats = originalChats.filter(chat => chat.id !== id);
    setChats(newChats);
    if (activeChatId === id) {
      if (newChats.length > 0) {
        setActiveChatId(newChats[0].id);
      } else {
        const newChat = createNewChat();
        setChats([newChat]);
        setActiveChatId(newChat.id);
      }
    }
    if (id.toString().startsWith('local-')) return;
    try {
      await api.delete(`/chats/${id}`);
    } catch (error) {
      console.error("Erro ao remover chat:", error);
      setChats(originalChats);
    }
  };

  const handleOpenSettings = (chatId) => {
    setEditingChatId(chatId);
  };
  
  const handleRenameChat = (chatId) => {
    setRenamingChatId(chatId);
  };

  const handleSaveChatTitle = async (chatId, newTitle) => {
    const originalTitle = chats.find(c => c.id === chatId)?.title;
    setRenamingChatId(null);
    setChats(prev => prev.map(c => c.id === chatId ? { ...c, title: newTitle } : c));
    try {
      await api.put(`/chats/${chatId}/title`, { title: newTitle });
    } catch (error) {
      console.error("Erro ao renomear o chat:", error);
      setChats(prev => prev.map(c => c.id === chatId ? { ...c, title: originalTitle } : c));
    }
  };

  const showContinueButton = (activeChat && activeChat.ingredients.length > 0 && activeChat.messages.length > 0 && canRegenerate) || (activeChat && activeChat.ingredients.length > 0 && activeChat.messages.length === 0);
  const isChatStarted = activeChat && activeChat.messages.length > 0;

  if (!activeChat) {
    return (
      <div className="flex items-center justify-center h-screen w-screen">
        <div className="rounded-full h-8 w-8 bg-primary animate-ping"></div>
      </div>
    );
  }

  return (
    <div className="flex h-dvh bg-bg">
       {isSidebarOpen && (
        <div
          onClick={() => setIsSidebarOpen(false)}
          className="fixed inset-0 bg-black bg-opacity-50 z-30 lg:hidden"
        />
       )}
       <Sidebar
        chats={chats} activeChatId={activeChatId} onNewChat={handleNewChat} onSelectChat={handleSelectChat}
        onFavoriteChat={handleFavoriteChat} onRemoveChat={handleRemoveChat} onOpenSettings={handleOpenSettings}
        isSidebarOpen={isSidebarOpen} setIsSidebarOpen={setIsSidebarOpen}
        renamingChatId={renamingChatId}
        onRenameChat={handleRenameChat}
        onSaveChatTitle={handleSaveChatTitle}
      />
      <div className="flex flex-col flex-grow items-center justify-between w-full min-w-0">
        {chatToEdit && (
          <SettingsModal
            isOpen={!!editingChatId} onClose={() => setEditingChatId(null)}
            settings={chatToEdit.settings} onSettingChange={handleSettingsChange}
          />
        )}
        <RecipeDetail recipe={selectedRecipe} onClose={() => setSelectedRecipe(null)} />
        <Header 
          isSidebarOpen={isSidebarOpen} onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} onLogout={logout}
        />
        
        {isChatStarted && activeChat.ingredients.length > 0 && (
          <div className="w-full max-w-2xl mt-4 px-2 md:px-4">
            <ParametersChips params={activeChat.ingredients} editable={true} onRemove={handleRemoveIngredient} />
          </div>
        )}

        <main ref={mainContainerRef} className="flex flex-col items-center w-full h-full my-4 overflow-y-auto px-2 md:px-4">
          {!isChatStarted && !isCurrentChatLoading ? (
            <div className="flex flex-col items-center justify-center text-center h-full">
              <div className="flex flex-col items-center justify-center gap-4">
                <Hello name={user?.name} />
                {activeChat.ingredients.length > 0 && (
                  <div className="w-full max-w-md pt-4">
                    <ParametersChips params={activeChat.ingredients} editable={true} onRemove={handleRemoveIngredient} />
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-start w-full max-w-2xl mt-6 space-y-4">
              {activeChat.messages.map((message, index) => {
                if (message.role === 'user') {
                  return <div key={index} className="self-end p-3 bg-primary text-light rounded-xl shadow-md text-sm max-w-lg">{message.content}</div>;
                }
                if (message.role === 'assistant') {
                  if (message.type === 'recipe-carousel') {
                    return <RecipeCarousel key={index} recipes={message.content} onSelectRecipe={setSelectedRecipe} />;
                  }
                  return <AIMessage key={index} message={message.content} />;
                }
                return null;
              })}
              {isCurrentChatLoading && (
                <div className="flex items-center justify-center w-12 h-12">
                   <div className="rounded-full h-4 w-4 bg-solid animate-ping"></div>
                </div>
              )}
            </div>
          )}
        </main>

        <div className="w-full max-w-2xl mb-2 px-2 md:px-4">
          <div className="flex flex-col items-end justify-center gap-4 w-full mt-auto">
             {showContinueButton && !isCurrentChatLoading && (
              <PrimaryButton onClick={handleGenerateRecipes}>
                Continuar
              </PrimaryButton>
            )}
            <MessageInput placeholder={!isChatStarted ? "Digite um ingrediente..." : "Peça uma alteração ou faça uma pergunta..."} disabled={isCurrentChatLoading} onSend={handleOnSend} />
          </div>
        </div>
      </div>
    </div>
  );
}