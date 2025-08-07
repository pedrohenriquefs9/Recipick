import { useState, useRef, useEffect } from "react";
import { PlusIcon } from "@heroicons/react/16/solid";

// --- ALTERAÇÃO 1: Importação do CameraIcon foi removida ---
// import { CameraIcon } from "@heroicons/react/24/outline";

export function MessageInput({
  onSend,
  placeholder = "O que você acha?",
  disabled = false,
}) {
  const [inputValue, setInputValue] = useState("");
  const inputRef = useRef(null);

  const focusInput = () => {
    setTimeout(() => {
      inputRef.current?.focus();
    }, 0);
  };

  useEffect(() => {
    focusInput();
  }, []);

  function handleSubmit(event) {
    event.preventDefault();
    onSend(inputValue.trim());
    setInputValue("");
    focusInput();
  }
  return (
    <div className="flex flex-col items-center justify-center gap-2 w-full">
      <form
        onSubmit={handleSubmit}
        className="flex items-center justify-between gap-2 w-full"
      >
        {}

        <div className="flex justify-between items-center w-full gap-1 text-black bg-solid rounded-full px-3 py-2">
          <input
            ref={inputRef}
            type="text"
            name="message"
            disabled={disabled}
            id="message"
            className="outline-0 w-full text-sm h-8 disabled:opacity-50"
            placeholder={placeholder}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
          {inputValue.trim().length !== 0 && (
            <button
              type="submit"
              disabled={disabled || inputValue.trim().length === 0}
              className="cursor-pointer rounded-full bg-solid-dark p-1 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <PlusIcon className="h-6 w-6 text-dark-light" />
            </button>
          )}
        </div>
      </form>
      <small className="text-[10px] text-center text-dark-light">
        O ReciPick pode cometer erros. Verifique as informações.
      </small>
    </div>
  );
}