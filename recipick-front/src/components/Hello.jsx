import clsx from "clsx";

export function Hello({ name, left = false }) {
  return (
    <div
      className={clsx(
        "flex flex-col justify-center gap-1",
        left ? "items-start" : "items-center"
      )}
    >
      <span
        className={clsx(
          "text-primary-dark text-3xl font-semibold",
          left ? "text-left" : "text-center"
        )}
      >
        Olá{name ? `, ${name}` : ""}!
      </span>
      <span className={clsx("text-black", left ? "text-left" : "text-center")}>
        Quais ingredientes você tem e o que quer comer hoje?
      </span>
    </div>
  );
}
