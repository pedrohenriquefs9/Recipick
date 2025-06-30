import { XMarkIcon } from "@heroicons/react/16/solid";

export function Chip({ children, removable = false, onRemove }) {
  return (
    <div className="flex gap-2 bg-solid text-black text-xs px-2 py-1 rounded-full">
      <span>
        {children}
      </span>
      {removable && (
        <button className="cursor-pointer" onClick={onRemove}>
          <XMarkIcon className="h-4 w-4 text-black" />
        </button>
      )}
    </div>
  );
}
