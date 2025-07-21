import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from './AuthContext';

export function ProtectedRoute({ children }) {
  const { token, loading } = useAuth();

  if (!token && loading) {
    // Se não houver token, redireciona para a página de boas-vindas
    return <Navigate to="/welcome" />;
  }

  return children;
}