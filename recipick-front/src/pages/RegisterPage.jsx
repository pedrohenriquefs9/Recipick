import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthLayout } from '../components/AuthLayout';
import { useAuth } from '../auth/AuthContext';

export function RegisterPage() {
  const [step, setStep] = useState(1); // 1: nome, 2: email/senha
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  
  const { register, loading, error } = useAuth();
  const navigate = useNavigate();

  const handleNextStep = (e) => {
    e.preventDefault();
    if (name.trim() !== '') {
      setStep(2);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert("As senhas não coincidem!");
      return;
    }
    await register(name, email, password);
    navigate('/');
  };

  return (
    <AuthLayout>
      <div className="flex flex-col items-center text-center">
        {step === 1 && (
          <>
            <h2 className="text-3xl font-semibold text-black">Como posso te chamar?</h2>
            <form onSubmit={handleNextStep} className="mt-8 flex w-full flex-col gap-4">
              <input 
                type="text" 
                placeholder="Seu nome" 
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full rounded-full bg-solid p-3 text-center text-black outline-none"
                required
              />
              <button type="submit" className="w-full rounded-full bg-primary p-3 text-center text-light font-semibold">
                Continuar
              </button>
            </form>
          </>
        )}

        {step === 2 && (
          <>
            <h2 className="text-3xl font-semibold text-black">Cadastro</h2>
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
              <input 
                type="password" 
                placeholder="Confirme sua senha" 
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full rounded-full bg-solid p-3 text-center text-black outline-none"
                required
              />
              {error && <p className="text-red-500 text-sm">{error}</p>}
              <button 
                type="submit" 
                className="w-full rounded-full bg-primary p-3 text-center text-light font-semibold"
                disabled={loading}
              >
                {loading ? 'Cadastrando...' : 'Finalizar Cadastro'}
              </button>
            </form>
          </>
        )}
        
        <Link to="/welcome" className="mt-4 text-sm text-dark-light">
          Voltar
        </Link>
      </div>
    </AuthLayout>
  );
}