import React, { createContext, useState, useContext, useEffect } from 'react';
import { api } from '../api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const verifySession = async () => {
      try {
        const response = await api.get('/auth/check_session');
        setUser(response.data);
      } catch (err) {
        setUser(null);
      } finally {
        setLoading(false);
      }
    };
    verifySession();
  }, []);

  const login = async (email, password) => {
    setLoading(true);
    setError('');
    try {
      const response = await api.post('/auth/login', { email, password });
      setUser(response.data.user);
      return true;
    } catch (err) {
      setError('Falha no login. Verifique as suas credenciais.');
      setUser(null);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      await api.post('/auth/logout');
    } catch (err) {
      console.error("Erro no logout:", err);
    } finally {
      setUser(null);
    }
  };
  
  const register = async (name, email, password) => {
    setLoading(true);
    setError('');
    try {
        await api.post('/auth/registrar', { name, email, password });
        return await login(email, password);
    } catch (err) {
        setError('Falha no registo. O email ou nome de utilizador pode já existir.');
        return false;
    } finally {
        setLoading(false);
    }
  };

  const value = { user, loading, error, login, logout, register };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}