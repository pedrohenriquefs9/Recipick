import axios from 'axios';

export const api = axios.create({
  // Revertendo para o endereço completo do backend
  baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  // Mantemos o withCredentials, pois é necessário para TENTAR enviar os cookies
  withCredentials: true,
});