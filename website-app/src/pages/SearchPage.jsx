import { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

function SearchPage() {
  const [stockList, setStockList] = useState([]);
  const [tickerInput, setTickerInput] = useState("");

  useEffect(() => {
    getStocks();
  }, []);

  const getStocks = () => {
    axios
      .get("/api/stocks")
      .then((res) => {
        console.log("stocks:", res.data);
        const stocks = res.data;
        setStockList(stocks);

        stocks.forEach((stock) => getPrice(stock));
      })
      .catch((err) => console.log(err));
  };

  const getPrice = (stock) => {
    axios
      .get(`/api/stocks/fetch_prev_close/?ticker=${stock.stock_ticker}`)
      .then((res) => {
        setStockList((prevList) =>
          prevList.map((item) =>
            item.id === stock.id
              ? { ...item, recent_price: res.data.prev_close }
              : item
          )
        );
      })
      .catch((err) => console.log(err));
  };

  const handleInputChange = (e) => {
    setTickerInput(e.target.value.toUpperCase());
  };

  const searchStock = () => {
    axios
      .get(`/api/stocks/search_for_stock/?ticker=${tickerInput}`)
      .then((res) => {
        setStockList((prevList) => {
          const exists = prevList.some(
            (s) =>
              s.stock_ticker.toUpperCase() ===
              res.data.stock_ticker.toUpperCase()
          );

          if (exists) {
            return prevList;
          }

          return [...prevList, res.data];
        });

        setTickerInput("");
      })
      .catch((err) => {
        console.error(err);
        alert("Stock not found");
      });
  };

  return (
    <div className="min-h-screen min-w-screen bg-gray-100 p-6">
      <div className="max-w-3xl mx-auto bg-white shadow-lg rounded-lg p-6">
        <h1 className="text-3xl mb-6 text-center text-gray-800">
          Search Ticker
        </h1>

        <div className="flex mb-6 gap-4">
          <input
            type="text"
            minLength={1}
            maxLength={5}
            value={tickerInput}
            onChange={handleInputChange}
            placeholder="Enter ticker"
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-800"
          />
          <button
            onClick={searchStock}
            className="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-4 py-2 rounded-lg transition-colors"
          >
            Search
          </button>
        </div>

        <ul className="space-y-4">
          {stockList.map((item) => (
            <li
              key={item.id}
              className="flex justify-between items-center bg-gray-50 p-4 rounded-lg shadow hover:bg-gray-100 transition"
            >
              <div>
                <span className="font-semibold text-gray-800">
                  {item.stock_ticker}
                </span>{" "}
                -{" "}
                <span className="text-green-600 font-medium">
                  ${item.recent_price ?? "N/A"}
                </span>
              </div>

              <Link to={`/stock/${item.stock_ticker}`}>
                <button className="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded-lg transition">
                  Financials
                </button>
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default SearchPage;