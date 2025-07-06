import { createContext, useContext, useReducer } from "react";

const initialState = {
  ingredients: [],
  messages: [],
  isLoading: false,
  error: null,
  // Podemos adicionar as configurações aqui no futuro
  settings: {
    style: "criativo",
    portionSize: "medio",
    complexity: "rapida",
    isVegetarian: false,
    restrictions: "",
  },
};

const AppContext = createContext();

function appReducer(state, action) {
  switch (action.type) {
    case "START_LOADING":
      return { ...state, isLoading: true, error: null };
    case "STOP_LOADING":
      return { ...state, isLoading: false };
    case "SET_ERROR":
      return { ...state, isLoading: false, error: action.payload };
    case "ADD_INGREDIENT":
      // Evita adicionar ingredientes duplicados ou vazios
      if (
        action.payload &&
        !state.ingredients.includes(action.payload.trim())
      ) {
        return { ...state, ingredients: [...state.ingredients, action.payload.trim()] };
      }
      return state;
    case "REMOVE_INGREDIENT":
      return {
        ...state,
        ingredients: state.ingredients.filter(
          (_, index) => index !== action.payload
        ),
      };
    case "ADD_MESSAGE":
      return {
        ...state,
        messages: [...state.messages, action.payload],
        isLoading: false,
      };
    case "CLEAR_MESSAGES":
        return { ...state, messages: [] };
    case "CLEAR_INGREDIENTS":
        return { ...state, ingredients: [] };
    default:
      throw new Error(`Ação não reconhecida: ${action.type}`);
  }
}

// 4. Criação do Provedor do Contexto
export function AppProvider({ children }) {
  const [state, dispatch] = useReducer(appReducer, initialState);

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}

// 5. Hook customizado para facilitar o uso do contexto
export function useAppState() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error("useAppState deve ser usado dentro de um AppProvider");
  }
  return context;
}