import React from 'react';
import { RecipeCard } from './RecipeDetail';

export function RecipeList({ recipes }) {
  if (!Array.isArray(recipes) || recipes.length === 0) {
    return <p className="text-center text-dark-light">Nenhuma receita para exibir.</p>;
  }

  return (
    <div className="flex flex-col gap-4 w-full">
      {recipes.map((recipe, index) => (
        <RecipeCard key={index} recipe={recipe} />
      ))}
    </div>
  );
}