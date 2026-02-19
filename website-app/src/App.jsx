import { Routes, Route } from "react-router-dom"
import Home from "./pages/Home"
import About from "./pages/About"
import SearchPage from "./pages/SearchPage";
import StockPageWrapper from "./pages/StockPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<SearchPage />}/>
      <Route path="/stock/:ticker" element={<StockPageWrapper />} />
    </Routes>
  );
}

export default App
