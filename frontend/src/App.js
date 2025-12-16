import React, { Component } from "react";
import axios from "axios";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      stockList: [],
      activeItem: {
        stock_ticker: "",
        stock_name: "",
        recent_price: 0.0,
      },
      ticker_input: "",
    };
  }

  componentDidMount() {
    this.getStocks();
  }

  getStocks() {
    axios
      .get("/api/stocks")
      .then((res) => {
        const stocks = res.data;

        this.setState({ stockList: stocks}, () => {
          stocks.forEach((stock) => this.getPrice(stock));
        });
      })
      .catch((err) => console.log(err));
  };

  getPrice(stock) {
    axios
      .get(`/api/stocks/fetch_prev_close/?ticker=${stock.stock_ticker}`)
      .then((res) => {
        this.setState((prevState) => ({
          stockList: prevState.stockList.map((item) =>
            item.id === stock.id
              ? { ...item, recent_price: res.data.prev_close }
              : item
          ),
        }));
      })
      .catch((err) => console.log(err));
  }

  handleInputChange = (e) => {
    this.setState({ ticker_input: e.target.value.toUpperCase() });
  };

  searchStock = () => {
    axios
      .get(`/api/stocks/search_for_stock/?ticker=${this.state.ticker_input}`)
      .then((res) => {
        this.setState((prevState) => {
          const exists = prevState.stockList.some(
            (s) => s.stock_ticker.toUpperCase() === res.data.stock_ticker.toUpperCase()
          );

          if (exists) {
            return {ticker_input: ""};
          }

          return {
            stockList: [...prevState.stockList, res.data],
            ticker_input: "",
          };
        });
      })
      .catch((err) => {
        console.error(err);
        alert("Stock not found");
      });
  };

  render() {
    return (
      <div>
          <h1>Stocks</h1>
          <div>
            <label>Enter a ticker: </label>
            <input 
              type="text" 
              minLength={1} 
              maxLength={5}
              value={this.state.ticker_input}
              onChange={this.handleInputChange}
            />
            <button onClick={this.searchStock}>Search</button>
          </div>
          <ul>
            {this.state.stockList.map((item) => (
              <li key={item.id}>{item.stock_ticker} - ${item.recent_price}</li>
            ))}
          </ul>
      </div>
    );
  }

}

export default App;