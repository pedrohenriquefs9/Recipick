import React from 'react';
import { XMarkIcon } from '@heroicons/react/24/outline';
import clsx from 'clsx';

export function SettingsModal({ onClose, settings, onSettingsChange }) {

  // Função para atualizar uma configuração chamando a função do componente pai
  const updateSetting = (key, value) => {
    onSettingsChange({ [key]: value });
  };

  const getButtonClass = (key, value) => clsx(
    'px-4 py-2 rounded-full text-sm font-semibold transition-colors',
    settings[key] === value 
      ? 'bg-primary-dark text-white' 
      : 'bg-solid hover:bg-solid-dark'
  );

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-20"
      onClick={onClose} // Fecha o modal ao clicar fora
    >
      {/* Container do Modal */}
      <div 
        className="bg-bg rounded-2xl shadow-xl p-6 w-full max-w-md mx-4 flex flex-col gap-8"
        onClick={(e) => e.stopPropagation()} // Impede que cliques dentro do modal o fechem
      >
        <header className="flex items-center justify-between">
          <h1 className="text-xl font-bold text-primary-dark">Configurações</h1>
          <button onClick={onClose} className="p-1 rounded-full hover:bg-solid">
            <XMarkIcon className="h-6 w-6 text-black" />
          </button>
        </header>

        {/* Conteúdo das Configurações */}
        <div className="flex flex-col gap-6">
          {/* Porção */}
          <div>
            <h2 className="font-semibold text-black mb-2">Tamanho da Porção</h2>
            <div className="flex gap-2">
              <button onClick={() => updateSetting('portionSize', 'pequeno')} className={getButtonClass('portionSize', 'pequeno')}>Pequeno</button>
              <button onClick={() => updateSetting('portionSize', 'medio')} className={getButtonClass('portionSize', 'medio')}>Médio</button>
              <button onClick={() => updateSetting('portionSize', 'grande')} className={getButtonClass('portionSize', 'grande')}>Grande</button>
            </div>
          </div>

          {/* Complexidade */}
          <div>
            <h2 className="font-semibold text-black mb-2">Complexidade da Receita</h2>
            <div className="flex gap-2">
              <button onClick={() => updateSetting('complexity', 'rapida')} className={getButtonClass('complexity', 'rapida')}>Rápida</button>
              <button onClick={() => updateSetting('complexity', 'elaborada')} className={getButtonClass('complexity', 'elaborada')}>Elaborada</button>
            </div>
          </div>
          
          {/* Estilo */}
          <div>
            <h2 className="font-semibold text-black mb-2">Estilo da Receita</h2>
            <div className="flex gap-2">
              <button onClick={() => updateSetting('style', 'popular')} className={getButtonClass('style', 'popular')}>Popular</button>
              <button onClick={() => updateSetting('style', 'criativo')} className={getButtonClass('style', 'criativo')}>Criativa</button>
            </div>
          </div>

          {/* Preferências Alimentares */}
          <div>
            <h2 className="font-semibold text-black mb-2">Preferências Alimentares</h2>
            <div className="flex flex-col gap-4">
              <label className="flex items-center justify-between bg-solid p-3 rounded-lg">
                <span className="font-medium">Sou vegetariano(a)</span>
                <div className="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" checked={settings.isVegetarian} onChange={(e) => updateSetting('isVegetarian', e.target.checked)} className="sr-only peer" />
                  <div className="w-11 h-6 bg-solid-dark rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-dark"></div>
                </div>
              </label>
              <textarea
                value={settings.restrictions}
                onChange={(e) => updateSetting('restrictions', e.target.value)}
                placeholder="Ex: Tenho alergia a camarão, não gosto de coentro..."
                className="w-full p-3 bg-solid rounded-lg outline-none focus:ring-2 focus:ring-primary-dark"
                rows="3"
              ></textarea>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}