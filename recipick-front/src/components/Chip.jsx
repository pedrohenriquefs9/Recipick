
export function Chip({ text, onRemove }) {
  return (
    <span className="inline-flex items-center bg-gray-200 text-sm text-gray-800 px-3 py-1 rounded-full mr-2 mb-2">
      {text}
      <button
        onClick={onRemove}
        className="ml-2 text-gray-600 hover:text-red-500 font-bold"
        aria-label="Remover"
      >
        ×
      </button>
    </span>
  );
}
