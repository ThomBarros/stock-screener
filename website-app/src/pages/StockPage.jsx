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
    <div className="min-h-screen min-w-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto bg-white shadow-lg rounded-lg p-6 space-y-6">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-800">{ticker}</h1>
          {price ? (
            <p className="text-xl mt-2 text-green-600">
              ${price.live_price} <span className="text-gray-500 text-sm">({lastUpdated})</span>
            </p>
          ) : (
            <p className="text-gray-500 mt-2">Loading live price...</p>
          )}
        </div>

        {/* Tearsheet Info */}
        <div>
          <h2 className="text-2xl font-semibold mb-2 text-gray-700">Tearsheet Info</h2>
          {tearsheetInfo ? (
            <div className="bg-gray-50 p-4 rounded-lg overflow-x-auto">
              <pre className="text-left text-sm text-gray-800">
                {JSON.stringify(tearsheetInfo, null, 2)}
              </pre>
            </div>
          ) : (
            <p className="text-gray-500">Loading tearsheet...</p>
          )}
        </div>

        {/* Financials */}
        <div>
          <h2 className="text-2xl font-semibold mb-2 text-gray-700">Financials</h2>
          {financials ? (
            <div className="bg-gray-50 p-4 rounded-lg overflow-x-auto">
              <pre className="text-left text-sm text-gray-800">
                {JSON.stringify(financials, null, 2)}
              </pre>
            </div>
          ) : (
            <p className="text-gray-500">Loading financials...</p>
          )}
        </div>
      </div>
    </div>
  );






}

export default StockPageWrapper;