import React, { createContext, useState, useContext } from 'react';
import { api } from '../api'; // Assumindo que seu api.js está em src/

// 1. Cria o Contexto
const AuthContext = createContext(null);

// 2. Cria o Provedor do Contexto
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token')); // Carrega o token do localStorage
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Configura o token em todas as chamadas da API
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`;

  const login = async (email, password) => {
    setLoading(true);
    setError('');
    try {
      // --- PONTO DE INTEGRAÇÃO PARA O BACKEND ---
      // const response = await api.post('/auth/login', { email, password });
      // const { token, user } = response.data;

      // ---- DADOS MOCKADOS (provisórios) ----
      const mockResponse = { token: 'fake-jwt-token', user: { name: 'João' } };
      const { token, user } = mockResponse;
      // ------------------------------------

      localStorage.setItem('token', token);
      setToken(token);
      setUser(user);
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } catch (err) {
      setError('Falha no login. Verifique suas credenciais.');
    } finally {
      setLoading(false);
    }
  };

  const register = async (name, email, password) => {
    setLoading(true);
    setError('');
    try {
      // --- PONTO DE INTEGRAÇÃO PARA O BACKEND ---
      // await api.post('/auth/registrar', { name, email, password });

      // Após o registro, faz o login automaticamente
      await login(email, password);
    } catch (err) {
      setError('Falha no cadastro. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
    delete api.defaults.headers.common['Authorization'];
  };

  const value = { user, token, loading, error, login, register, logout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// 3. Hook customizado para usar o contexto facilmente
export function useAuth() {
  return useContext(AuthContext);
}