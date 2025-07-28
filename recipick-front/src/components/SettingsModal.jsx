import React from 'react';
import { XMarkIcon } from '@heroicons/react/24/solid';

// Componente auxiliar para os botões de opção, para manter o código limpo
function SettingOption({ label, isActive, onClick }) {
  const baseClasses = "px-4 py-2 rounded-full text-sm font-semibold transition-colors duration-200";
  const activeClasses = "bg-primary text-light";
  const inactiveClasses = "bg-solid hover:bg-solid-dark";

  return (
    <button
      type="button"
      className={`${baseClasses} ${isActive ? activeClasses : inactiveClasses}`}
      onClick={onClick}
    >
      {label}
    </button>
  );
}

export function SettingsModal({ isOpen, onClose, settings, onSettingChange }) {
  if (!isOpen) {
    return null;
  }

  // Função para lidar com a mudança de uma configuração específica
  const handleOptionClick = (key, value) => {
    onSettingChange({ ...settings, [key]: value });
  };

  return (
    // Fundo semi-transparente que cobre a tela inteira
    <div 
      className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center p-4 z-50"
      onClick={onClose} // Fecha o modal se clicar no fundo
    >
      {/* O painel de configurações */}
      <div 
        className="bg-bg rounded-2xl shadow-lg p-6 w-full max-w-md"
        onClick={(e) => e.stopPropagation()} // Impede que o clique dentro do modal o feche
      >
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-primary-dark">Configurações</h2>
          <button onClick={onClose} className="p-1 rounded-full hover:bg-solid">
            <XMarkIcon className="h-6 w-6 text-black" />
          </button>
        </div>

        {/* Grupos de Configurações */}
        <div className="space-y-5">
          <div>
            <h3 className="font-semibold mb-2">Dieta da receita</h3>
            <div className="flex flex-wrap gap-2">
              <SettingOption label="Onívora" isActive={settings.diet === 'omnivore'} onClick={() => handleOptionClick('diet', 'omnivore')} />
              <SettingOption label="Vegetariana" isActive={settings.diet === 'vegetarian'} onClick={() => handleOptionClick('diet', 'vegetarian')} />
              <SettingOption label="Vegana" isActive={settings.diet === 'vegan'} onClick={() => handleOptionClick('diet', 'vegan')} />
            </div>
          </div>
          <div>
            <h3 className="font-semibold mb-2">Complexidade da Receita</h3>
            <div className="flex flex-wrap gap-2">
              <SettingOption label="Rápida" isActive={settings.complexity === 'rapida'} onClick={() => handleOptionClick('complexity', 'rapida')} />
              <SettingOption label="Elaborada" isActive={settings.complexity === 'elaborada'} onClick={() => handleOptionClick('complexity', 'elaborada')} />
            </div>
          </div>
          <div>
            <h3 className="font-semibold mb-2">Estilo da receita</h3>
            <div className="flex flex-wrap gap-2">
              <SettingOption label="Popular" isActive={settings.style === 'popular'} onClick={() => handleOptionClick('style', 'popular')} />
              <SettingOption label="Criativa" isActive={settings.style === 'criativo'} onClick={() => handleOptionClick('style', 'criativo')} />
            </div>
          </div>
          <div>
            <h3 className="font-semibold mb-2">Tamanho da Porção</h3>
            <div className="flex flex-wrap gap-2">
              <SettingOption label="Pequena" isActive={settings.portionSize === 'pequeno'} onClick={() => handleOptionClick('portionSize', 'pequeno')} />
              <SettingOption label="Média" isActive={settings.portionSize === 'medio'} onClick={() => handleOptionClick('portionSize', 'medio')} />
              <SettingOption label="Grande" isActive={settings.portionSize === 'grande'} onClick={() => handleOptionClick('portionSize', 'grande')} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}