export function PrimaryButton({ children, onClick }) {
  return (
    <button type="button" onClick={onClick} className="cursor-pointer p-2 bg-primary rounded-full inline-flex justify-center items-center text-center text-light">
      {children}
    </button>
  );
}
