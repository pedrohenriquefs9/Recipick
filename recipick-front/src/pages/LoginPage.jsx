import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthLayout } from '../components/AuthLayout';
import { useAuth } from '../auth/AuthContext';

export function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login, loading, error } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault(); // Impede o recarregamento da página
    await login(email, password);
    // Após o login (mesmo que mockado), o AuthContext terá o token,
    // e o ProtectedRoute fará o redirecionamento automático.
    // Adicionamos uma navegação explícita para garantir.
    navigate('/'); 
  };

  return (
    <AuthLayout>
      <div className="flex flex-col items-center text-center">
        <h2 className="text-3xl font-semibold text-black">Login</h2>
        <form onSubmit={handleSubmit} className="mt-8 flex w-full flex-col gap-4">
          <input 
            type="email" 
            placeholder="E-mail" 
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full rounded-full bg-solid p-3 text-center text-black outline-none"
            required
          />
          <input 
            type="password" 
            placeholder="Senha" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full rounded-full bg-solid p-3 text-center text-black outline-none"
            required
          />
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <button 
            type="submit" 
            className="w-full rounded-full bg-primary p-3 text-center text-light font-semibold"
            disabled={loading}
          >
            {loading ? 'Entrando...' : 'Continuar'}
          </button>
        </form>
        <Link to="/welcome" className="mt-4 text-sm text-dark-light">
          Voltar
        </Link>
      </div>
    </AuthLayout>
  );
}