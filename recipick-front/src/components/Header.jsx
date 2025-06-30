import { Cog6ToothIcon } from "@heroicons/react/24/outline";
import { Link } from "react-router";

export function Header() {
  return (
    <header className="flex w-full items-center justify-between py-4 pt-14">
      <Link to="/">
        <img src="/logo.svg" />
      </Link>
      <Link to="/settings" className="cursor-pointer">
        <Cog6ToothIcon className="h-6 w-6 text-black" />
      </Link>
    </header>
  );
}
