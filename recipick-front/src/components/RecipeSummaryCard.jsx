import React from 'react';

export function RecipeSummaryCard({ recipe, onSelect }) {
  const hasImage = recipe.imagemUrl;

  return (
    <div
      onClick={() => onSelect(recipe)}
      className="relative flex flex-col justify-end w-44 h-44 flex-shrink-0 bg-solid rounded-2xl p-4 cursor-pointer shadow-md hover:shadow-lg hover:scale-105 transition-transform duration-200 overflow-hidden text-white"
    >
      {hasImage ? (
        <img 
          src={recipe.imagemUrl} 
          alt={recipe.titulo}
          className="absolute inset-0 w-full h-full object-cover z-0"
          onError={(e) => { e.target.style.display = 'none'; }}
        />
      ) : (
        <div className="absolute inset-0 w-full h-full bg-solid-dark z-0"></div>
      )}
      
      <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/40 to-transparent z-10"></div>
      
      <h3 className="relative z-20 font-bold text-base line-clamp-3">{recipe.titulo}</h3>
    </div>
  );
}