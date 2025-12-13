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
    };
  }

  componentDidMount() {
    this.getStocks();
  }

  getStocks() {
    axios
      .get("/api/stocks")
      .then((res) => this.setState({ stockList: res.data}))
      .catch((err) => console.log(err));
  };

  render() {
    return (
      <div>
          <h1>Stocks</h1>
          <ul>
            {this.state.stockList.map((item) => (
              <li key={item.id}>{item.stock_ticker}</li>
            ))}
          </ul>
      </div>
    );
  }

}

export default App;