import React from 'react';
import { Link } from 'react-router-dom';
import { AuthLayout } from '../components/AuthLayout';

export function WelcomePage() {
  return (
    <AuthLayout>
      <div className="flex w-full flex-col gap-4">
        <Link to="/login">
          <button className="w-full rounded-full bg-primary p-3 text-center text-light font-semibold">
            Login
          </button>
        </Link>
        <Link to="/registrar">
          <button className="w-full rounded-full bg-solid p-3 text-center text-black font-semibold">
            Cadastrar-se
          </button>
        </Link>
      </div>
    </AuthLayout>
  );
}