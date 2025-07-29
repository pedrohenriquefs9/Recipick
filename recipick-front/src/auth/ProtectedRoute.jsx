import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from './AuthContext';

export function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) {
    return null; // Evita renderizar a página antes da verificação da sessão
  }

  // Se, após a verificação, não houver utilizador, redireciona
  if (!user) {
    return <Navigate to="/welcome" replace />;
  }

  // Se houver utilizador, mostra a página protegida
  return children;
}