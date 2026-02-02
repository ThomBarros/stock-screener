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
  const [description, setDescription] = useState(null);
  const [name, setName] = useState(null);
  const [currency, setCurrency] = useState(null);
  const [website, setWebsite] = useState(null);
  const [sector, setSector] = useState(null);
  const [industry, setIndustry] = useState(null);
  const [phone, setPhone] = useState(null);
  const [employees, setEmployees] = useState(null);
  const [country, setCountry] = useState(null);
  const [enterpriseValue, setEnterpriseValue] = useState(null);

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
      .then((res) => {
        setTearsheetInfo(res.data);
        setDescription(res.data.tearsheet_info.description);
        setName(res.data.tearsheet_info.name);
        setCurrency(res.data.tearsheet_info.currency);
        setWebsite(res.data.tearsheet_info.website);
        setSector(res.data.tearsheet_info.sector);
        setIndustry(res.data.tearsheet_info.industry);
        setPhone(res.data.tearsheet_info.phone);
        setEmployees(res.data.tearsheet_info.employees);
        setCountry(res.data.tearsheet_info.country);
        setEnterpriseValue(res.data.tearsheet_info.enterprise_value);
      })
      .catch((err) => console.error(err))
  }, [ticker]);

  return (
    <div className="min-h-screen min-w-screen bg-gray-100 p-6">
      <div className="w-[90vw] mx-auto bg-white shadow-lg rounded-lg p-6 space-y-6">

        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-800">{name} ({ticker})</h1>
          {price ? (
            <p className="text-xl mt-2 text-green-600">
              {currency}${price.live_price} <span className="text-gray-500 text-sm">({lastUpdated})</span>
            </p>
          ) : (
            <p className="text-gray-500 mt-2">Loading live price...</p>
          )}
        </div>

        <div>
          <h2 className="text-2xl font-semibold mb-2 text-gray-700">Business Description</h2>
          <p className="text-gray-800 text-left text-sm">{description}</p>
        </div>

        <div>
          <h2 className="text-2xl font-semibold mb-2 text-gray-700">Key Info</h2>
          <p className="text-gray-800 text-left text-sm">
            Website: <a href={website} target="_blank" rel="noopener noreferrer">{website}</a>
          </p>
          <p className="text-gray-800 text-left text-sm">Phone: {phone}</p>
          <p className="text-gray-800 text-left text-sm">Industry: {industry}</p>
          <p className="text-gray-800 text-left text-sm">Sector: {sector}</p>
          <p className="text-gray-800 text-left text-sm">Number of employees: {employees}</p>
          <p className="text-gray-800 text-left text-sm">Country: {country}</p>
        </div>

        <div>
          <h2 className="text-2xl font-semibold mb-2 text-gray-700">Key Financials</h2>
          <p className="text-gray-800 text-left text-sm">Enterprise value: {enterpriseValue}</p>
        </div>

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