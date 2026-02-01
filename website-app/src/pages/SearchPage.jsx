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
    <div>
      <h1>Search Stocks</h1>

      <div>
        <label>Enter a ticker: </label>
        <input
          type="text"
          minLength={1}
          maxLength={5}
          value={tickerInput}
          onChange={handleInputChange}
        />
        <button onClick={searchStock}>Search</button>
      </div>

      <ul>
        {stockList.map((item) => (
          <li key={item.id}>
            {item.stock_ticker} - ${item.recent_price}
            <Link to={`/stock/${item.stock_ticker}`}>
              <button>Financials</button>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SearchPage;
