import clsx from "clsx";

export function Button({ children, onClick, variant = "primary", ...props }) {
  const variants = {
    primary: "bg-primary text-light",
  };

  return (
    <button
      type="button"
      onClick={onClick}
      className={clsx(
        `cursor-pointer p-2 rounded-full inline-flex justify-center items-center text-center`,
        variants[variant],
        "hover:opacity-90 transition-opacity duration-200",
        "focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary",
        "disabled:opacity-50 disabled:cursor-not-allowed",
      )}
      {...props}
    >
      {children}
    </button>
  );
}
