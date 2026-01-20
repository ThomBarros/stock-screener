import { Routes, Route } from "react-router-dom";
import SearchPage from "./pages/SearchPage";
import StockPageWrapper from "./pages/StockPage";

const Main = () => (
  <Routes>
    <Route path="/" element={<SearchPage />} />
    <Route path="/stock/:ticker" element={<StockPageWrapper />} />
  </Routes>
);

export default Main;
