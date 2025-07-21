import React, { useRef, useState } from 'react';
import { RecipeSummaryCard } from './RecipeSummaryCard';

export function RecipeCarousel({ recipes, onSelectRecipe }) {
  const carouselRef = useRef(null);
  const [isDown, setIsDown] = useState(false);
  const [startX, setStartX] = useState(0);
  const [scrollLeft, setScrollLeft] = useState(0);
  const [isDragging, setIsDragging] = useState(false);

  if (!Array.isArray(recipes) || recipes.length === 0) {
    return null;
  }

  const handleMouseDown = (e) => {
    setIsDown(true);
    carouselRef.current.classList.add('active');
    setStartX(e.pageX - carouselRef.current.offsetLeft);
    setScrollLeft(carouselRef.current.scrollLeft);
    setIsDragging(false);
  };

  const handleMouseLeave = () => {
    setIsDown(false);
    carouselRef.current.classList.remove('active');
  };

  const handleMouseUp = () => {
    setIsDown(false);
    carouselRef.current.classList.remove('active');
  };

  const handleMouseMove = (e) => {
    if (!isDown) return;
    e.preventDefault();
    setIsDragging(true);
    const x = e.pageX - carouselRef.current.offsetLeft;
    const walk = (x - startX);
    carouselRef.current.scrollLeft = scrollLeft - walk;
  };

  const handleCardClick = (recipe) => {
    if (isDragging) {
      return;
    }
    onSelectRecipe(recipe);
  };

  return (
    <div className="w-full">
      <p className="text-dark-light mb-4">Beleza! Com base nisso, tenho algumas sugestões:</p>
      <div
        // Adicionada a classe 'select-none' para impedir a seleção de texto
        className="flex gap-4 overflow-x-auto pb-4 cursor-grab select-none"
        ref={carouselRef}
        onMouseDown={handleMouseDown}
        onMouseLeave={handleMouseLeave}
        onMouseUp={handleMouseUp}
        onMouseMove={handleMouseMove}
      >
        {recipes.map((recipe, index) => (
          <RecipeSummaryCard
            key={index}
            recipe={recipe}
            onSelect={handleCardClick}
          />
        ))}
      </div>
    </div>
  );
}