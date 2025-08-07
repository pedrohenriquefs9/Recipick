import { Bars3Icon } from "@heroicons/react/24/outline";
import { Link } from "react-router-dom";
import { ProfileDropdown } from "./ProfileDropdown";

export function Header({ isSidebarOpen, onToggleSidebar, onLogout }) {
  return (
    <header className="flex w-full items-center justify-between py-4 pt-8 px-4">
      <div className="flex items-center gap-4">
        {!isSidebarOpen && (
          <button onClick={onToggleSidebar} className="p-1 rounded-md hover:bg-gray-200">
            <Bars3Icon className="h-6 w-6 text-black" />
          </button>
        )}
        <Link to="/">
          <img src="/logo.svg" alt="ReciPick Logo" />
        </Link>
      </div>
      
      <ProfileDropdown onLogout={onLogout} />
    </header>
  );
}