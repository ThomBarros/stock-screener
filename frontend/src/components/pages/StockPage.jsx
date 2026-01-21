import React, { Component } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

function StockPageWrapper() {
  const { ticker } = useParams();
  return <StockPage ticker={ticker} />;
}

class StockPage extends Component {
  state = {
    financials: null,
  };

  componentDidMount() {
    this.fetchFinancials();
  }

  fetchConsolidatedFinancials() {
    axios
      .get(`/api/stocks/fetch_financial_info/?ticker=${this.props.ticker}&consolidated=true`)
      .then((res) => {
        this.setState({ financials: res.data});
      })
      .catch((err) => console.error(err));
  }

  fetchFinancials() {
    axios
      .get(`/api/stocks/fetch_financial_info/?ticker=${this.props.ticker}&consolidated=true`)
      .then((res) => {
        this.setState({ financials: res.data });
      })
      .catch((err) => console.error(err));
  }

  render() {
    const { ticker } = this.props;
    const { financials } = this.state;

    return (
      <div>
        <h1>Financials for {ticker}</h1>
        {financials ? (
          <pre style={{ textAlign: "left" }}>
            {JSON.stringify(financials, null, 2)}
          </pre>
        ) : (
          <p>Loading...</p>
        )}
      </div>
    );
  }
}

export default StockPageWrapper;
