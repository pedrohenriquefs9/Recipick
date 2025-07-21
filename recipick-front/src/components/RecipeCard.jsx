import React from 'react';

export function RecipeCard({ recipe }) {
  // Se não houver uma receita, não renderiza nada.
  if (!recipe) {
    return null;
  }

  return (
    <div className="border rounded-lg p-4 shadow-md bg-white">
      <img src={recipe.image} alt={recipe.title} className="w-full h-40 object-cover rounded-t-lg" />
      <div className="p-2">
        <h3 className="text-xl font-bold mb-2">{recipe.title}</h3>
        <p className="text-gray-700">{recipe.description}</p>
      </div>
    </div>
  );
}