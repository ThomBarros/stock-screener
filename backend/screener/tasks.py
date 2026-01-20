import requests
import pandas as pd
from collections import Counter
from typing import Dict, List, Tuple


HEADERS = {
    "User-Agent": "User Name username@example.com"
}

SEC_TICKER_CIK_URL = "https://www.sec.gov/files/company_tickers.json"
COMPANY_FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{}.json"

EXCLUDE_PATTERNS = (
    "Abstract",
    "TextBlock",
    "Policy",
    "Disclosure",
    "Table",
    "Axis",
    "Domain",
    "Member",
)

BALANCE_SHEET_KEYWORDS = (
    "Asset",
    "Liabilit",
    "Equity",
    "Receivable",
    "Payable",
    "Inventory",
    "Cash",
    "Debt",
    "Deferred",
)

INCOME_STATEMENT_KEYWORDS = (
    "Revenue",
    "Expense",
    "Income",
    "Earnings",
    "Loss",
    "Profit",
    "Tax",
    "Interest",
)

CASH_FLOW_KEYWORDS = (
    "Cash",
    "OperatingActivities",
    "InvestingActivities",
    "FinancingActivities",
    "Payments",
    "Proceeds",
)

ANCHORS = {
    "Balance Sheet": ["Assets"],
    "Income Statement": ["Revenues", "NetIncomeLoss"],
    "Cash Flow Statement": ["NetCashProvidedByUsedInOperatingActivities"],
}

EXCLUDE_PATTERNS = (
    "Abstract",
    "TextBlock",
    "Policy",
    "Disclosure",
    "Table",
    "Axis",
    "Domain",
    "Member",
)


def is_numeric_tag(tag: str) -> bool:
    return not any(p in tag for p in EXCLUDE_PATTERNS)


def is_valid_period(item: dict, statement: str) -> bool:
    """
    Balance Sheet -> instant (no 'start')
    Income / Cash Flow -> duration (has 'start')
    """
    has_start = "start" in item

    if statement == "Balance Sheet":
        return not has_start
    return has_start


def is_consolidated(item: dict) -> bool:
    return not item.get("segments")


def get_cik_from_ticker(ticker: str) -> str:
    resp = requests.get(SEC_TICKER_CIK_URL, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()

    for company in data.values():
        if company["ticker"].upper() == ticker.upper():
            return str(company["cik_str"]).zfill(10)

    raise ValueError(f"Ticker not found: {ticker}")


def get_company_facts(cik: str) -> dict:
    url = COMPANY_FACTS_URL.format(cik)
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def classify_statement(tag: str) -> str | None:
    if any(k in tag for k in BALANCE_SHEET_KEYWORDS):
        return "Balance Sheet"
    if any(k in tag for k in INCOME_STATEMENT_KEYWORDS):
        return "Income Statement"
    if any(k in tag for k in CASH_FLOW_KEYWORDS):
        return "Cash Flow Statement"
    return None


def detect_anchor(facts: dict, statement: str) -> Tuple[str, str]:
    """
    Returns (accession, period_end) for the primary statement.
    """
    gaap = facts["facts"]["us-gaap"]
    candidates = []

    for anchor_tag in ANCHORS[statement]:
        tag_data = gaap.get(anchor_tag)
        if not tag_data:
            continue

        for items in tag_data.get("units", {}).values():
            for item in items:
                if not item.get("form", "").startswith("10-K"):
                    continue
                if not is_consolidated(item):
                    continue
                if not is_valid_period(item, statement):
                    continue

                candidates.append((item["accn"], item["end"]))

    if not candidates:
        raise RuntimeError(f"No anchor found for {statement}")

    # Pick the most frequent (accn, end) pair -> primary statement
    return Counter(candidates).most_common(1)[0][0]


def extract_primary_statement(facts: dict, statement: str) -> pd.DataFrame:
    gaap = facts["facts"]["us-gaap"]
    accn, period_end = detect_anchor(facts, statement)

    rows = []

    for tag, tag_data in gaap.items():
        if not is_numeric_tag(tag):
            continue

        for unit, items in tag_data.get("units", {}).items():
            for item in items:
                if item.get("accn") != accn:
                    continue
                if item.get("end") != period_end:
                    continue
                if not item.get("form", "").startswith("10-K"):
                    continue
                if not is_consolidated(item):
                    continue
                if not is_valid_period(item, statement):
                    continue

                rows.append({
                    "tag": tag,
                    "value": item.get("val"),
                    "unit": unit,
                    "period_start": item.get("start"),
                    "period_end": item.get("end"),
                    "fiscal_year": item.get("fy"),
                    "accession": item.get("accn"),
                })

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("tag").reset_index(drop=True)

    return df


def extract_financial_statements(facts: dict) -> Dict[str, pd.DataFrame]:
    gaap_facts = facts.get("facts", {}).get("us-gaap", {})

    statements: Dict[str, List[dict]] = {
        "Balance Sheet": [],
        "Income Statement": [],
        "Cash Flow Statement": [],
    }

    for tag, tag_data in gaap_facts.items():
        if not is_numeric_tag(tag):
            continue

        statement = classify_statement(tag)
        if not statement:
            continue

        for unit, items in tag_data.get("units", {}).items():
            for item in items:
                if not item.get("form", "").startswith("10-K"):
                    continue

                if not is_valid_period(item, statement):
                    continue

                statements[statement].append({
                    "tag": tag,
                    "value": item.get("val"),
                    "unit": unit,
                    "period_start": item.get("start"),
                    "period_end": item.get("end"),
                    "fiscal_year": item.get("fy"),
                    "accession": item.get("accn"),
                })

    # Convert to DataFrames
    dfs = {}
    for name, rows in statements.items():
        df = pd.DataFrame(rows)
        if not df.empty:
            df = df.sort_values(
                ["fiscal_year", "period_end", "tag"],
                ascending=[False, False, True]
            ).reset_index(drop=True)
        dfs[name] = df

    return dfs


def get_sec_primary_financials(ticker: str):
    cik = get_cik_from_ticker(ticker)
    facts = get_company_facts(cik)

    return {
        "Income Statement": extract_primary_statement(facts, "Income Statement"),
        "Balance Sheet": extract_primary_statement(facts, "Balance Sheet"),
        "Cash Flow Statement": extract_primary_statement(facts, "Cash Flow Statement"),
    }


def get_sec_financials(ticker: str):
    cik = get_cik_from_ticker(ticker)
    facts = get_company_facts(cik)
    statements = extract_financial_statements(facts)
    return statements


if __name__ == "__main__":
    statements = get_sec_financials("AAPL")
    primary_statements = get_sec_primary_financials("AAPL")

    for name, df in statements.items():
        print(f"\n{name}")
        print(df.head(15))

    for name, df in primary_statements.items():
        print(f"\n{name}")
        print(df.head(15))