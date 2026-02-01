import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

function StockPageWrapper() {
  const { ticker } = useParams();
  return <StockPage ticker={ticker} />;
}

function StockPage({ ticker }) {
  const [financials, setFinancials] = useState(null);
  const [price, setPrice] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [tearsheetInfo, setTearsheetInfo] = useState(null);

  useEffect(() => {
    axios
      .get(`/api/stocks/fetch_financial_info/?ticker=${ticker}&consolidated=true`)
      .then((res) => setFinancials(res.data))
      .catch((err) => console.error(err));
  }, [ticker]);

  useEffect(() => {
    const fetchPrice = () => {
      axios
        .get(`/api/stocks/fetch_live_price/?ticker=${ticker}`)
        .then((res) => {
          setPrice(res.data);
          setLastUpdated(new Date().toLocaleTimeString());
        })
        .catch((err) => console.error(err));
    };

    fetchPrice();
    const interval = setInterval(fetchPrice, 5000);

    return () => clearInterval(interval);
  }, [ticker]);

  useEffect(() => {
    axios
      .get(`/api/stocks/fetch_tearsheet_info/?ticker=${ticker}`)
      .then((res) => setTearsheetInfo(res.data))
      .catch((err) => console.error(err))
  }, [ticker]);

  return (
    <div>
      <h1>{ticker}</h1>
      {price ? (
        <div>
          <p>Price: { price.live_price }</p>
          <p>Last Updated: { lastUpdated }</p>
        </div>
      ) : (
        <p>Loading live price...</p>
      )}
      <h2>Tearsheet Info</h2>
      <div>
        { tearsheetInfo ? (
        <pre> {JSON.stringify(tearsheetInfo, null, 2)}</pre>
        ) : (
          <p>Loading tearsheet...</p>
        )}
      </div>
      <h2>Financials</h2>
      {financials ? (
        <pre style={{ textAlign: "left" }}>{JSON.stringify(financials, null, 2)}</pre>
      ) : (
        <p>Loading financials...</p>
      )}
    </div>
  );
}

export default StockPageWrapper;