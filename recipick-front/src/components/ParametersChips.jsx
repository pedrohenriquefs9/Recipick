
import { Chip } from "./Chip";

export function ParametersChips({ params, onRemove }) {
  return (
    <div className="flex flex-wrap mt-2 gap-1">
      {params.map((param, index) => (
        <Chip key={index} text={param} onRemove={() => onRemove(index)} />
      ))}
    </div>
  );
}
