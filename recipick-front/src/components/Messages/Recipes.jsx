import { useEffect, useMemo } from 'react';
import { ImageAPI } from '../../imageAPI';
import { Button } from '../Button';
import { RecipeCard } from './RecipeCard';

export function Recipes({ recipes, isLoading, onRegenerate, onRecipeClick }) {
  const imageAPI = useMemo(() => new ImageAPI(), []);

  useEffect(() => {
    if (recipes.length > 0) {
      recipes.forEach(async (recipe) => {
        if (!recipe.imageURL) {
          const imageURL = await imageAPI.fetchFoodImage(recipe.title);
          recipe.imageURL = imageURL;
        }
      });
    }
  }, [recipes, imageAPI]);

  return (
    <div className="flex flex-col items-center justify-center gap-4 w-full">
      {recipes.length > 0 && !isLoading ? (
        <div className="flex gap-4 w-full overflow-x-auto pb-5 scrollbar-thin p-2">
          {recipes.map((recipe, index) => (
            <div key={index} className="flex-shrink-0 min-w-64">
              <RecipeCard
                title={recipe.title}
                content={recipe.content}
                imageURL={recipe.imageURL}
                onClick={() => onRecipeClick(recipe)}
              />
            </div>
          ))}
          {onRegenerate && (
            <div className="flex-shrink-0 min-w-64">
              <RegenerateButton />
            </div>
          )}
        </div>
      ) : (
        <div className="flex items-center justify-center w-full h-48">
          {isLoading ? (
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-solid border-primary"></div>
          ) : (
            <div className="flex flex-col items-center justify-center gap-2">
              <p className="text-gray-500">Nenhuma receita disponível</p>
              {onRegenerate && (
                <Button onClick={onRegenerate}>Tentar novamente</Button>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function RegenerateButton({ onClick }) {
  return (
    <button
      onClick={onClick}
      className="bg-solid shadow-md rounded-2xl p-4 flex flex-col items-center justify-center gap-2 w-full cursor-pointer hover:shadow-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary h-full min-h-[200px] hover:bg-solid-dark"
    >
      <svg
        className="w-12 h-12 text-primary"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
        />
      </svg>
      <span className="text-center font-medium">Tentar novamente</span>
    </button>
  );
}
