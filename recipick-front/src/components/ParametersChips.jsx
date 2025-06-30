import { Chip } from "./Chip";

export function ParametersChips({ params = [], editable = false, onRemove }) {
  return (
    <div className="flex flex-wrap w-full gap-2">
      {params.map((param, index) => (
        <Chip key={index} removable={editable} onRemove={() => onRemove(index)}>
          {param}
        </Chip>
      ))}
    </div>
  );
}
