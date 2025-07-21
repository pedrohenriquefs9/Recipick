// pedrohenriquefs9/recipick/Recipick-a523c06ee35576e2de28a874a6a6746518831ecf/recipick-front/src/components/RecipeList.jsx

import React from 'react';
import { RecipeCard } from './RecipeCard';

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