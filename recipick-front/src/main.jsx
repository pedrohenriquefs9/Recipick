import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";

import "./index.css";
import Home from "./Home.jsx";
// A importação de Settings foi removida daqui

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        {/* A rota "/settings" foi REMOVIDA daqui */}
      </Routes>
    </BrowserRouter>
  </StrictMode>
);