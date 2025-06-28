import { XMarkIcon } from "@heroicons/react/16/solid";

export function Chip({ children, removable = false }) {
  return (
    <div className="flex gap-2 bg-solid text-black text-xs px-2 py-1 rounded-full">
      <span>
        {children}
      </span>
      {removable && (
        <button className="cursor-pointer">
          <XMarkIcon className="h-4 w-4 teext-black" />
        </button>
      )}
    </div>
  );
}
