import { Chip } from "./components/Chip";
import { Header } from "./components/Header";
import { Hello } from "./components/Hello";
import { ParametersChips } from "./components/ParametersChips";
import { MessageInput } from "./MessageInput";

export function Home() {
  return (
    <div className="flex flex-col items-center justify-between bg-bg px-4 h-screen">
      <Header />
      <main className="flex flex-col items-center h-screen mb-6">
        <div className="h-full flex flex-col items-center justify-center">
          <div className="flex flex-col items-center justify-center gap-4">
            <Hello name="João" />
            <ParametersChips
              params={["arroz", "feijão", "frango", "batata"]}
              editable={true}
            />
          </div>
        </div>
        <MessageInput />
      </main>
    </div>
  );
}
