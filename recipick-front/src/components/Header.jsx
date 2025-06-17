import { Cog6ToothIcon } from "@heroicons/react/24/outline";
import { Link } from "react-router-dom";
import logo from "../assets/logo.svg";

export function Header({ onSettingsClick }) { 
  return (
    <header className="flex w-full items-center justify-between py-4 pt-14">
      <Link to="/">
        {/* Apenas uma imagem do logo deve estar aqui */}
        <img src={logo} alt="ReciPick Logo" />
      </Link>
      
      <button 
        onClick={onSettingsClick} 
        className="cursor-pointer p-2 -mr-2 rounded-full hover:bg-solid transition-colors duration-200"
      >
        <Cog6ToothIcon className="h-6 w-6 text-black" />
      </button>
      {/* A tag extra de fechamento </button> foi removida daqui */}
    </header>
  );
}