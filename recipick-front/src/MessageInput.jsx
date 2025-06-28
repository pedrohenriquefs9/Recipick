import { PlusIcon } from "@heroicons/react/16/solid";
import { CameraIcon } from "@heroicons/react/24/outline";

export function MessageInput() {
  function handleSubmit(event) {
    event.preventDefault();
  }
  return (
    <div className="flex flex-col items-center justify-center gap-2 w-full">
      <form
        onSubmit={handleSubmit}
        className="flex items-center justify-between gap-2 w-full"
      >
        <button
          type="button"
          className="flex flex-shrink-0 cursor-pointer items-center justify-center rounded-full bg-solid p-1 h-12 w-12"
        >
          <CameraIcon className="text-black w-7 h-7" />
        </button>
        <div className="flex justify-between items-center w-full gap-1 text-black bg-solid rounded-full px-3 py-2">
          <input
            type="text"
            name="message"
            id="message"
            className="outline-0 w-full text-sm"
            placeholder="Digite um ingrediente ou preferência"
          />
          <button
            type="submit"
            className="cursor-pointer rounded-full bg-solid-dark p-1"
          >
            <PlusIcon className="h-6 w-6 text-dark-light" />
          </button>
        </div>
      </form>
      <small className="text-[10px] text-center text-dark-light">O ReciPick pode cometer erros. Verifique as informações.</small>
    </div>
  );
}
