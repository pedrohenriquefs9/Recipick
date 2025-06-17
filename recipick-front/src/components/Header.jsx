import { Cog6ToothIcon } from "@heroicons/react/24/outline";
import { Link } from "react-router-dom";
import logo from "../assets/logo.svg"; // Importando o logo

export function Header({ onSettingsClick }) { 
  return (
    <header className="flex w-full items-center justify-between py-4 pt-14">
      <Link to="/">
        <img src={logo} alt="ReciPick Logo" />
      </Link>
      
      {/* O botão de configurações será modificado em um commit futuro */}
      <button 
        onClick={onSettingsClick} 
        className="cursor-pointer p-2 -mr-2 rounded-full hover:bg-solid transition-colors duration-200"
      >
        <Cog6ToothIcon className="h-6 w-6 text-black" />
      </button>
    </header>
  );
}