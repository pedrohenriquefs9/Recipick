import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthLayout } from '../components/AuthLayout';
import { useAuth } from '../auth/AuthContext';

// Regex para validação de e-mail no frontend
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function RegisterPage() {
  const [step, setStep] = useState(1);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  
  const [formError, setFormError] = useState('');
  
  // Renomeando 'error' do useAuth para 'apiError' para evitar conflitos
  const { register, loading, error: apiError } = useAuth();
  const navigate = useNavigate();

  const handleNextStep = (e) => {
    e.preventDefault();
    if (name.trim() !== '') {
      setFormError(''); // Limpa erros anteriores
      setStep(2);
    } else {
      setFormError('Por favor, insira seu nome.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError(''); // Limpa erros de formulário antes de submeter

    // --- ALTERAÇÃO 2: Adicionar validações no frontend ---
    if (!EMAIL_REGEX.test(email)) {
      setFormError("Por favor, insira um e-mail válido.");
      return;
    }
    if (password.length < 6 || password.length > 14) {
      setFormError("A senha deve ter entre 6 e 14 caracteres.");
      return;
    }
    if (password !== confirmPassword) {
      setFormError("As senhas não coincidem!");
      return;
    }
    // --- FIM DA VALIDAÇÃO ---

    const wasSuccessful = await register(name, email, password);
    if (wasSuccessful) {
        navigate('/');
    }
    // Se 'register' retornar false, o 'apiError' no hook useAuth será exibido
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
              {/* Exibe erro de validação do passo 1 */}
              {formError && <p className="text-red-500 text-sm">{formError}</p>}
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
              {/* --- ALTERAÇÃO 3: Exibir o erro de validação do formulário OU o erro vindo da API --- */}
              {(formError || apiError) && <p className="text-red-500 text-sm">{formError || apiError}</p>}
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