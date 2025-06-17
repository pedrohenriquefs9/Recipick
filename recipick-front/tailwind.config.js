/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#D4760B',
        'primary-dark': '#8F5008',
        'black': '#222221',
        'light': '#FFFAFA',
        'solid': {
          DEFAULT: '#D3CEC9',
          'dark': '#BEB7AE',
        },
        'dark-light': '#565453',
        'bg': '#F4F1EE',
      },
    },
  },
  plugins: [],
}