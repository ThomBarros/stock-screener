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
  const [fullExchangeName, setFullExchangeName] = useState(null); 

  const [enterpriseValue, setEnterpriseValue] = useState(null);
  const [totalDebt, setTotalDebt] = useState(null);
  const [totalRevenue, setTotalRevenue] = useState(null);
  const [totalCash, setTotalCash] = useState(null);
  const [ebitda, setEbitda] = useState(null);
  const [volume, setVolume] = useState(null);
  const [sharesOutstanding, setSharesOutstanding] = useState(null);

  const [beta, setBeta] = useState(null);
  const [dividendRate, setDividendRate] = useState(null);
  const [dividendYield, setDividendYield] = useState(null);
  const [payoutRatio, setPayoutRatio] = useState(null);
  const [bookValue, setBookValue] = useState(null);
  const [priceToBook, setPriceToBook] = useState(null);  
  const [netIncomeToCommon, setNetIncomeToCommon] = useState(null);

  const [quickRatio, setQuickRatio] = useState(null);
  const [currentRatio, setCurrentRatio] = useState(null);

  const [debtToEquity, setDebtToEquity] = useState(null);
  const [revenuePerShare, setRevenuePerShare] = useState(null);
  const [returnOnAssets, setReturnOnAssets] = useState(null);
  const [returnOnEquity, setReturnOnEquity] = useState(null);
  const [grossProfits, setGrossProfits] = useState(null);

  const [enterpriseToRevenue, setEnterpriseToRevenue] = useState(null);
  const [enterpriseToEbitda, setEnterpriseToEbitda] = useState(null);
  const [epsCurrentYear, setEpsCurrentYear] = useState(null);

  const [earningsGrowth, setEarningsGrowth] = useState(null);
  const [revenueGrowth, setRevenueGrowth] = useState(null);

  const [grossMargins, setGrossMargins] = useState(null);
  const [ebitdaMargins, setEbitdaMargins] = useState(null);
  const [operatingMargins, setOperatingMargins] = useState(null);

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
        setFullExchangeName(res.data.tearsheet_info.full_Exchange_Name);
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
        setDividendRate(res.data.tearsheet_info.dividend_Rate);
        setDividendYield(res.data.tearsheet_info.dividend_Yield);
        setTotalDebt(res.data.tearsheet_info.total_Debt);
        setTotalRevenue(res.data.tearsheet_info.total_Revenue);
        setTotalCash(res.data.tearsheet_info.total_Cash);
        setEbitda(res.data.tearsheet_info.ebitda);
        setVolume(res.data.tearsheet_info.volume);
        setSharesOutstanding(res.data.tearsheet_info.shares_Outstanding);

        setBeta(res.data.tearsheet_info.beta);
        setPayoutRatio(res.data.tearsheet_info.payout_Ratio);
        setBookValue(res.data.tearsheet_info.book_Value);

        setPriceToBook(res.data.tearsheet_info.price_To_Book);
        setNetIncomeToCommon(res.data.tearsheet_info.net_Income_To_Common);
        setEnterpriseToRevenue(res.data.tearsheet_info.enterprise_To_Revenue);
        setEnterpriseToEbitda(res.data.tearsheet_info.enterprise_To_Ebitda);
        setQuickRatio(res.data.tearsheet_info.quick_Ratio);
        setCurrentRatio(res.data.tearsheet_info.current_Ratio);
        setDebtToEquity(res.data.tearsheet_info.debt_To_Equity);
        setRevenuePerShare(res.data.tearsheet_info.revenue_Per_Share);
        setReturnOnAssets(res.data.tearsheet_info.return_On_Assets);
        setReturnOnEquity(res.data.tearsheet_info.return_On_Equity);
        setGrossProfits(res.data.tearsheet_info.gross_Profits);
      })
      .catch((err) => console.error(err))
  }, [ticker]);




  return (
    <div className="min-h-screen min-w-screen bg-gray-100 p-6">
      <div className="w-[90vw] mx-auto bg-white shadow-lg rounded-lg p-6 space-y-6">

        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-800">{name} ({fullExchangeName}:{ticker})</h1>
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
          <h2 className="text-2xl font-semibold mb-2 text-gray-700">Info</h2>

         <div>
         <table class="table-auto w-full">
          <thead className="text-gray-800 text-center bg-gray-200">
            <tr>
              <th>Exchange</th>
              <th>Website</th>
              <th>Phone</th>
              <th>Industry/Sector</th>
              <th>Number of employees</th>
              <th>Country</th>
            </tr>
          </thead>
          <tbody className="text-gray-800 text-center bg-gray-100">
            <tr>
              <td>{fullExchangeName}</td>
              <td>
                <a href={website} target="_blank" rel="noopener noreferrer">{website}</a>
              </td>
              <td>{phone}</td>
              <td>{industry}/{sector}</td>
              <td>{employees}</td>
              <td>{country}</td>
            </tr>
          </tbody>
        </table>  
        </div>
        </div>


        <div>
          <h2 className="text-2xl font-semibold mb-2 text-gray-700">Financials</h2>
          <div>
          <table class="table-auto w-full">
          <thead className="text-gray-800 text-center bg-gray-200">
          </thead>
          <tbody className="text-gray-800 text-left bg-gray-100">
            <tr className="bg-gray-200">
              <th>Beta</th>
              <td>{beta}</td>
              <th>Enterprise to Revenue</th>
              <td>{enterpriseToRevenue}</td>
            </tr>
            <tr>
              <th>Payout Ratio</th>
              <td>{payoutRatio}</td>
              <th>Enterprise to EBITDA</th>
              <td>{enterpriseToEbitda}</td>
            </tr>
            <tr className="bg-gray-200">
              <th>Book Value</th>
              <td>{bookValue}</td>
              <th>Quick Ratio</th>
              <td>{quickRatio}</td>
            </tr>
            <tr>
              <th>Dividend Yield</th>
              <td>{dividendYield}</td>
              <th>Current Ratio</th>
              <td>{currentRatio}</td>
            </tr>
            <tr className="bg-gray-200">  
              <th>Dividend Rate</th>
              <td>{dividendRate}</td>
              <th>Debt to Equity</th>
              <td>{debtToEquity}</td>
            </tr>
            <tr>
              <th>Price to Book</th>
              <td>{priceToBook}</td>
              <th>Revenue per Share</th>
              <td>{revenuePerShare}</td>
            </tr>
            <tr className="bg-gray-200">
              <th>Return on Assets</th>
              <td>{returnOnAssets}</td>
              <th>Return on Equity</th>
              <td>{returnOnEquity}</td>
            </tr>
            <tr>
              <th>Gross Profits</th>
              <td>{grossProfits}</td>
              <th>Total Debt</th>
              <td>{totalDebt}</td>
            </tr>
            <tr className="bg-gray-200">
              <th>Total Revenue</th>
              <td>{totalRevenue}</td>
              <th>Total Cash</th>
              <td>{totalCash}</td>
            </tr>
            <tr>
              <th>Enterprise Value</th>
              <td>{enterpriseValue}</td>
              <th>EBITDA</th>
              <td>{ebitda}</td>
            </tr>
            <tr className="bg-gray-200">
              <th>Shares Outstanding</th>
              <td>{sharesOutstanding}</td>
              <th>Volume</th>
              <td>{volume}</td>
            </tr>
          </tbody>
        </table>  
        </div> 
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
