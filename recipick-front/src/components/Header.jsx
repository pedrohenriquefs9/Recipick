import { Cog6ToothIcon } from "@heroicons/react/24/outline";
import { Link } from "react-router-dom";

// A única alteração é que ele agora recebe a função 'onSettingsClick'
export function Header({ onSettingsClick }) {
  return (
    <header className="flex w-full items-center justify-between py-4 pt-8">
      <Link to="/">
        <img src="/logo.svg" alt="ReciPick Logo" />
      </Link>
      {/* O Link foi trocado por um botão para chamar a função */}
      <button type="button" onClick={onSettingsClick} className="cursor-pointer">
        <Cog6ToothIcon className="h-6 w-6 text-black" />
      </button>
    </header>
  );
}