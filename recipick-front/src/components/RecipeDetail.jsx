import React from 'react';
import { ArrowLeftIcon } from '@heroicons/react/24/solid';

export function RecipeDetail({ recipe, onClose }) {
  if (!recipe) {
    return null;
  }

  // Função para fechar ao clicar no fundo (overlay)
  const handleOutsideClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-60 flex justify-center items-center p-4 z-50 animate-fade-in"
      onClick={handleOutsideClick} // Adicionado o evento de clique aqui
    >
      <div 
        className="bg-solid text-black rounded-xl shadow-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto animate-scale-up"
        // Impede que cliques dentro do card fechem o modal
        onClick={(e) => e.stopPropagation()}
      >
        <button 
          onClick={onClose} 
          className="flex items-center gap-2 text-sm font-semibold text-primary-dark mb-4 hover:underline"
        >
          <ArrowLeftIcon className="h-5 w-5" />
          Voltar
        </button>

        <h2 className="text-2xl font-bold text-primary-dark mb-2">{recipe.titulo || 'Receita'}</h2>
        
        {recipe.inspiracao && (
          <p className="text-base text-dark-light mb-3">
            <strong>Inspiração:</strong> {recipe.inspiracao}
          </p>
        )}

        <div className="text-sm text-dark-light mb-4">
          {recipe.tempoDePreparoEmMin && <span><strong>Tempo:</strong> {recipe.tempoDePreparoEmMin} min | </span>}
          {recipe.porcoes && <span><strong>Porções:</strong> {recipe.porcoes}</span>}
        </div>

        {}
        {recipe.imagemUrl && (
            <img
              src={recipe.imagemUrl}
              alt={recipe.titulo}
              className="w-full h-64 object-cover rounded-lg my-4" // my-4 adiciona margem
            />
        )}

        <hr className="border-t-1 border-solid-dark my-4" />
        
        <div>
          <h3 className="font-bold text-lg mb-3">Ingredientes:</h3>
          <ul className="list-disc list-inside text-base space-y-2">
            {recipe.ingredientes?.map((ing, index) => (
              <li key={index}>
                {`${ing.quantidade || ''} ${ing.unidadeMedida || ''} de ${ing.nome || 'Ingrediente'}`.trim()}
              </li>
            ))}
          </ul>
        </div>

        <hr className="border-t-1 border-solid-dark my-4" />

        <div>
          <h3 className="font-bold text-lg mb-3">Modo de preparo:</h3>
          <ol className="list-decimal list-inside text-base space-y-3">
            {recipe.preparo?.map((step, index) => (
              <li key={index}>{step}</li>
            ))}
          </ol>
        </div>
      </div>
    </div>
  );
}