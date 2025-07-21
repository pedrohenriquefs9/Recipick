import React from 'react';

export function AuthLayout({ children }) {
  return (
    <div className="flex h-screen w-screen bg-bg">
      {/* Painel Esquerdo (Laranja) */}
      <div className="flex w-full flex-col items-center justify-center bg-primary lg:w-1/2">
        <h1 className="text-5xl font-bold text-light">ReciPick</h1>
        <p className="mt-2 text-lg text-light">Seu melhor amigo na cozinha</p>
      </div>
      
      {/* Painel Direito (Conteúdo) */}
      <div className="hidden w-1/2 flex-col items-center justify-center p-8 lg:flex">
        <div className="w-full max-w-sm">
          {children}
        </div>
      </div>
    </div>
  );
}