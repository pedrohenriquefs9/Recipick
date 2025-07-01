import { useState } from 'react';
import { Header } from './components/Header';
import { Hello } from './components/Hello';
import { ParametersChips } from './components/ParametersChips';
import { MessageInput } from './MessageInput';
import { Button } from './components/Button';
import { api } from './api';
import { AIMessage } from './components/Messages/AIMessage';
import { RecipeCard } from './components/Messages/RecipeCard';
import { Recipes } from './components/Messages/Recipes';

const recipesGeneratedMessages = [
  'Beleza! Com base nisso, tenho algumas sugestões: ',
  'Encontrei algumas receitas que podem ser feitas com os ingredientes que você forneceu. Veja abaixo:',
  'Aqui estão algumas receitas que você pode fazer com os ingredientes que você mencionou:',
  'Com esses ingredientes, você pode preparar as seguintes receitas:',
  'Ótimo! Com esses ingredientes, você pode fazer as seguintes receitas:',
  'Com esses ingredientes, você pode preparar as seguintes receitas deliciosas:',
  'Com esses ingredientes, você pode fazer as seguintes receitas incríveis:',
];

export function Home() {
  const [ingredients, setIngredients] = useState([]);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  function getRandomRecipeMessage() {
    const randomIndex = Math.floor(Math.random() * recipesGeneratedMessages.length);
    return recipesGeneratedMessages[randomIndex];
  }

  async function handleGenerateRecipes() {
    if (ingredients.length === 0) {
      return;
    }
    try {
      setIsLoading(true);
      // TODO: It don't make sense to make an extra request to normalize ingredients
      // We can just send the ingredients directly to the recipe generation endpoint
      const { data } = await api.post('/normalizar-ingredientes', {
        ingredientes: ingredients,
      });
      const response = await api.post('/receitas', {
        ingredientes: data.ingredientes_normalizados
          .filter((ingredient) => ingredient.trim() !== '')
          .join(', '),
      });

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: getRandomRecipeMessage(),
        },
        {
          role: 'assistant-recipes',
          content: response.data.receitas,
        },
      ]);
    } catch (error) {
      console.error('Erro ao normalizar ingredientes:', error);
      alert('Ocorreu um erro ao processar os ingredientes. Tente novamente.');
    } finally {
      setIsLoading(false);
    }
  }

  function handleAddIngredient(newIngredient) {
    if (!newIngredient || newIngredient.trim() === '') {
      return;
    }
    setIngredients((prev) => [...prev, newIngredient]);
  }

  function handleRefineRecipes(message) {
    setMessages((prev) => [
      ...prev,
      {
        role: 'user',
        content: message,
      },
    ]);

    console.log('Refinando receitas com a mensagem:', message);
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
      <main className="flex flex-col items-center h-full mb-6 max-w-full">
        <div className="h-full flex flex-col items-center justify-center">
          <div className="flex flex-col items-center justify-center gap-4">
            <Hello />
            <ParametersChips
              params={ingredients}
              editable={messages.length === 0 && !isLoading}
              onRemove={(index) => {
                setIngredients((prev) => prev.filter((_, i) => i !== index));
              }}
            />
          </div>
        </div>
        <div className="flex flex-col items-start justify-center w-full max-w-full mt-6">
          {(messages.length > 0 || isLoading) && (
            <div className="flex flex-col items-start justify-center gap-4 mt-6 max-w-full">
              {messages.map((message, index) =>
                message.role == 'assistant' ? (
                  <AIMessage key={index} message={message.content} />
                ) : message.role == 'assistant-recipes' ? (
                  <Recipes
                    // recipes={message.content.recipes}
                    key={index}
                    recipes={[
                      {
                        title: 'Pão de Queijo',
                        content: 'Esta é uma receita de teste.',
                      },
                      {
                        title: 'Torta de Chocolate',
                        content: 'Esta é outra receita de teste.',
                      },
                    ]}
                    isLoading={isLoading}
                    onRegenerate={() => console.log('Regenerating recipes...')}
                    onRecipeClick={(recipe) => {
                      console.log('Recipe clicked:', recipe);
                    }}
                  />
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
            <Button onClick={handleGenerateRecipes}>Continuar</Button>
          )}
          <MessageInput
            placeholder={
              messages.length == 0
                ? 'Digite um ingrediente ou preferência'
                : 'O que você acha?'
            }
            disabled={isLoading}
            onSend={handleOnSend}
          />
        </div>
      </main>
    </div>
  );
}
