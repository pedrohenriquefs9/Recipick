import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from './AuthContext';

export function ProtectedRoute({ children }) {
  const { token } = useAuth();

  if (!token) {
    // Se não houver token, redireciona para a página de boas-vindas
    return <Navigate to="/welcome" />;
  }

  return children;
}