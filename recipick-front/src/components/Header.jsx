// pedrohenriquefs9/recipick/Recipick-a523c06ee35576e2de28a874a6a6746518831ecf/recipick-front/src/components/Header.jsx

import { Cog6ToothIcon } from "@heroicons/react/24/outline";
import { Link } from "react-router";

export function Header() {
  return (
    // Alterado de 'pt-14' para 'pt-8' para subir o header
    <header className="flex w-full items-center justify-between py-4 pt-8">
      <Link to="/">
        <img src="/logo.svg" />
      </Link>
      <Link to="/settings" className="cursor-pointer">
        <Cog6ToothIcon className="h-6 w-6 text-black" />
      </Link>
    </header>
  );
}