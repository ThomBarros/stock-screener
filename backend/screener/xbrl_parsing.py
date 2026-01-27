############################ 2 ##################################


# import json
# import requests
# from arelle import Cntlr
# from collections import defaultdict
# from bs4 import BeautifulSoup

# # ---------------------------
# # 1️⃣ Fetch XBRL model from SEC
# # ---------------------------
# def fetch_10k_xbrl_model(cik: str, year: int):
#     """
#     Fetch the 10-K XBRL filing from the SEC and load it into Arelle.
#     """
#     cik = str(cik).lstrip("0")
#     headers = {"User-Agent": "Your Name contact@example.com"}

#     # Company submissions JSON
#     submissions_url = f"https://data.sec.gov/submissions/CIK{int(cik):010d}.json"
#     resp = requests.get(submissions_url, headers=headers)
#     resp.raise_for_status()
#     data = resp.json()

#     filings = data.get("filings", {}).get("recent", {})
#     target_acc = None
#     for form, acc_no, fdate in zip(filings["form"], filings["accessionNumber"], filings["filingDate"]):
#         if form == "10-K" and fdate.startswith(str(year)):
#             target_acc = acc_no
#             break

#     if not target_acc:
#         raise RuntimeError(f"No 10-K filing found for CIK {cik} in {year}")

#     acc_no_no_dashes = target_acc.replace("-", "")
#     filing_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_no_no_dashes}/"

#     # Find XBRL instance file
#     resp = requests.get(filing_url, headers=headers)
#     resp.raise_for_status()
#     soup = BeautifulSoup(resp.text, "html.parser")

#     xbrl_file_url = None
#     for link in soup.find_all("a"):
#         href = link.get("href", "")
#         if href.endswith(".xml") and all(x not in href.lower() for x in ["cal", "def", "lab"]):
#             xbrl_file_url = "https://www.sec.gov" + href if href.startswith("/") else filing_url + href
#             break

#     if not xbrl_file_url:
#         raise RuntimeError("Could not find XBRL instance document.")

#     # Load into Arelle
#     cntlr = Cntlr.Cntlr(logFileName="logToPrint")
#     xbrl_model = cntlr.modelManager.load(xbrl_file_url)
#     if xbrl_model is None:
#         raise RuntimeError("Failed to load XBRL instance into Arelle")

#     return xbrl_model

# # ---------------------------
# # 2️⃣ Helper: get human-readable label
# # ---------------------------
# def get_fact_label(fact):
#     """
#     Fetch human-readable label from label linkbase.
#     Fallback to concept name if label not found.
#     """
#     concept = fact.concept
#     try:
#         label = concept.label("http://www.xbrl.org/2003/role/label", "en")
#     except Exception:
#         label = None
#     if not label:
#         label = concept.qname.localName
#     return label

# # ---------------------------
# # 3️⃣ Extract hierarchical numeric financial statements
# # ---------------------------
# def extract_financial_statements(xbrl_model):
#     """
#     Build hierarchical Balance Sheet, Income Statement, Cash Flow.
#     Only numeric facts are included.
#     """
#     statements = {
#         "BalanceSheet": defaultdict(dict),
#         "IncomeStatement": defaultdict(dict),
#         "CashFlowStatement": defaultdict(dict)
#     }

#     for fact in xbrl_model.facts:
#         # Skip non-numeric facts (text, tables, enumerations)
#         if not fact.isNumeric:
#             continue

#         label = get_fact_label(fact)
#         value = fact.value
#         tag_lower = fact.qname.localName.lower()

#         # -------------------
#         # Balance Sheet
#         # -------------------
#         if any(k in tag_lower for k in ["asset", "liability", "equity"]):
#             parent = "Assets" if "asset" in tag_lower else \
#                      "Liabilities" if "liability" in tag_lower else "Equity"
#             statements["BalanceSheet"][parent][label] = value

#         # -------------------
#         # Income Statement
#         # -------------------
#         elif any(k in tag_lower for k in ["revenue", "income", "expense", "profit", "loss"]):
#             if "revenue" in tag_lower:
#                 parent = "Revenue"
#             elif "expense" in tag_lower:
#                 parent = "Expenses"
#             else:
#                 parent = "NetIncome"
#             statements["IncomeStatement"][parent][label] = value

#         # -------------------
#         # Cash Flow Statement
#         # -------------------
#         elif "cash" in tag_lower:
#             if "operating" in tag_lower:
#                 parent = "OperatingActivities"
#             elif "investing" in tag_lower:
#                 parent = "InvestingActivities"
#             elif "financing" in tag_lower:
#                 parent = "FinancingActivities"
#             else:
#                 parent = "OtherCashFlows"
#             statements["CashFlowStatement"][parent][label] = value

#     # Convert defaultdicts to dicts
#     statements["BalanceSheet"] = {k: dict(v) for k, v in statements["BalanceSheet"].items()}
#     statements["IncomeStatement"] = {k: dict(v) for k, v in statements["IncomeStatement"].items()}
#     statements["CashFlowStatement"] = {k: dict(v) for k, v in statements["CashFlowStatement"].items()}

#     return statements

# # ---------------------------
# # 4️⃣ Example usage
# # ---------------------------
# if __name__ == "__main__":
#     cik = "0000320193"  # Apple
#     year = 2025

#     print("Fetching 10-K filing from SEC...")
#     xbrl_model = fetch_10k_xbrl_model(cik, year)

#     print("Extracting hierarchical numeric financial statements...")
#     statements = extract_financial_statements(xbrl_model)

#     output_file = "financial_statements_hierarchical_numeric.json"
#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(statements, f, indent=2, ensure_ascii=False)

#     print(f"✅ Done! Clean numeric statements saved to {output_file}")


# ############# 3 #################


# import requests
# from arelle import Cntlr
# from collections import defaultdict
# import json
# from bs4 import BeautifulSoup

# # ---------------------------
# # 1️⃣ Fetch 10-K XBRL/iXBRL filing from SEC
# # ---------------------------
# def fetch_10k_xbrl_model(cik: str, year: int):
#     cik = str(cik).lstrip("0")
#     headers = {"User-Agent": "Your Name contact@example.com"}

#     submissions_url = f"https://data.sec.gov/submissions/CIK{int(cik):010d}.json"
#     resp = requests.get(submissions_url, headers=headers)
#     resp.raise_for_status()
#     data = resp.json()

#     filings = data.get("filings", {}).get("recent", {})
#     target_acc = None
#     for form, acc_no, fdate in zip(filings["form"], filings["accessionNumber"], filings["filingDate"]):
#         if form == "10-K" and fdate.startswith(str(year)):
#             target_acc = acc_no
#             break

#     if not target_acc:
#         raise RuntimeError(f"No 10-K filing found for CIK {cik} in {year}")

#     acc_no_no_dashes = target_acc.replace("-", "")
#     filing_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_no_no_dashes}/"

#     resp = requests.get(filing_url, headers=headers)
#     resp.raise_for_status()
#     soup = BeautifulSoup(resp.text, "html.parser")

#     xbrl_file_url = None
#     for link in soup.find_all("a"):
#         href = link.get("href", "")
#         if href.endswith(".xml") and all(x not in href.lower() for x in ["cal", "def", "lab"]):
#             xbrl_file_url = "https://www.sec.gov" + href if href.startswith("/") else filing_url + href
#             break

#     if not xbrl_file_url:
#         raise RuntimeError("Could not find XBRL instance document.")

#     cntlr = Cntlr.Cntlr(logFileName="logToPrint")
#     xbrl_model = cntlr.modelManager.load(xbrl_file_url)
#     if xbrl_model is None:
#         raise RuntimeError("Failed to load XBRL instance into Arelle")

#     return xbrl_model

# # ---------------------------
# # 2️⃣ Hierarchical extraction with recursive subcategories
# # ---------------------------
# def build_recursive_hierarchy(facts, keywords):
#     """
#     Recursively build nested hierarchy from facts based on keyword groups.
#     """
#     tree = {}
#     for key, subkeys in keywords.items():
#         matching_facts = [f for f in facts if key.lower() in f.concept.qname.localName.lower() and f.isNumeric]
#         subtree = {}
#         # Recursively process subkeys
#         if subkeys:
#             subtree = build_recursive_hierarchy(matching_facts, subkeys)
#         # Add remaining facts under this key
#         for f in matching_facts:
#             subtree[f.concept.qname.localName] = f.value
#         if subtree:
#             tree[key] = subtree
#     return tree

# def extract_hierarchical_statements_ixbrl(xbrl_model):
#     """
#     Extract top-level financial statements hierarchically with subcategories.
#     """
#     # Define top-level and subcategories based on common GAAP keywords
#     hierarchy = {
#         "BalanceSheet": {
#             "Assets": {"CurrentAssets": {}, "NoncurrentAssets": {}},
#             "Liabilities": {"CurrentLiabilities": {}, "NoncurrentLiabilities": {}},
#             "Equity": {}
#         },
#         "IncomeStatement": {
#             "Revenue": {},
#             "Expenses": {},
#             "NetIncomeLoss": {}
#         },
#         "CashFlowStatement": {
#             "Operating": {},
#             "Investing": {},
#             "Financing": {}
#         }
#     }

#     statements = {}
#     for stmt_name, keywords in hierarchy.items():
#         statements[stmt_name] = build_recursive_hierarchy(xbrl_model.facts, keywords)

#     return statements

# # ---------------------------
# # 3️⃣ Main
# # ---------------------------
# if __name__ == "__main__":
#     cik = "0000320193"  # Apple
#     year = 2025

#     print("Fetching 10-K filing from SEC...")
#     xbrl_model = fetch_10k_xbrl_model(cik, year)

#     print("Extracting hierarchical financial statements...")
#     statements = extract_hierarchical_statements_ixbrl(xbrl_model)

#     # Save as JSON
#     output_file = "financial_statements_hierarchical.json"
#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(statements, f, indent=2, ensure_ascii=False)

#     print(f"✅ Done! Hierarchical statements saved to {output_file}")


# ####################### 4 ###################################


# import requests
# from arelle import Cntlr
# from bs4 import BeautifulSoup
# import json

# # ---------------------------
# # 1️⃣ Fetch 10-K XBRL/iXBRL filing from SEC
# # ---------------------------
# def fetch_10k_xbrl_model(cik: str, year: int):
#     cik = str(cik).lstrip("0")
#     headers = {"User-Agent": "Your Name contact@example.com"}

#     submissions_url = f"https://data.sec.gov/submissions/CIK{int(cik):010d}.json"
#     resp = requests.get(submissions_url, headers=headers)
#     resp.raise_for_status()
#     data = resp.json()

#     filings = data.get("filings", {}).get("recent", {})
#     target_acc = None
#     for form, acc_no, fdate in zip(filings["form"], filings["accessionNumber"], filings["filingDate"]):
#         if form == "10-K" and fdate.startswith(str(year)):
#             target_acc = acc_no
#             break

#     if not target_acc:
#         raise RuntimeError(f"No 10-K filing found for CIK {cik} in {year}")

#     acc_no_no_dashes = target_acc.replace("-", "")
#     filing_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_no_no_dashes}/"

#     resp = requests.get(filing_url, headers=headers)
#     resp.raise_for_status()
#     soup = BeautifulSoup(resp.text, "html.parser")

#     xbrl_file_url = None
#     for link in soup.find_all("a"):
#         href = link.get("href", "")
#         if href.endswith(".xml") and all(x not in href.lower() for x in ["cal", "def", "lab"]):
#             xbrl_file_url = "https://www.sec.gov" + href if href.startswith("/") else filing_url + href
#             break

#     if not xbrl_file_url:
#         raise RuntimeError("Could not find XBRL instance document.")

#     cntlr = Cntlr.Cntlr(logFileName="logToPrint")
#     xbrl_model = cntlr.modelManager.load(xbrl_file_url)
#     if xbrl_model is None:
#         raise RuntimeError("Failed to load XBRL instance into Arelle")

#     return xbrl_model

# # ---------------------------
# # 2️⃣ Helper to get human-readable label
# # ---------------------------
# def get_label(fact):
#     try:
#         return fact.concept.label()  # iXBRL human-readable label
#     except Exception:
#         return fact.concept.qname.localName  # fallback to concept name

# # ---------------------------
# # 3️⃣ Recursive hierarchical extraction
# # ---------------------------
# def build_recursive_hierarchy(facts, keywords):
#     tree = {}
#     for key, subkeys in keywords.items():
#         # Find facts matching this category
#         matching_facts = [f for f in facts if key.lower() in f.concept.qname.localName.lower() and f.isNumeric]
#         subtree = {}

#         # Recurse into subkeys
#         if subkeys:
#             subtree = build_recursive_hierarchy(matching_facts, subkeys)

#         # Add remaining facts under this key
#         for f in matching_facts:
#             subtree[get_label(f)] = f.value

#         if subtree:
#             tree[key] = subtree
#     return tree

# def extract_hierarchical_statements_ixbrl(xbrl_model):
#     # Top-level + common subcategories for human-readable structure
#     hierarchy = {
#         "BalanceSheet": {
#             "Assets": {"CurrentAssets": {}, "NoncurrentAssets": {}},
#             "Liabilities": {"CurrentLiabilities": {}, "NoncurrentLiabilities": {}},
#             "Equity": {}
#         },
#         "IncomeStatement": {
#             "Revenue": {},
#             "Expenses": {},
#             "NetIncomeLoss": {}
#         },
#         "CashFlowStatement": {
#             "Operating": {},
#             "Investing": {},
#             "Financing": {}
#         }
#     }

#     statements = {}
#     for stmt_name, keywords in hierarchy.items():
#         statements[stmt_name] = build_recursive_hierarchy(xbrl_model.facts, keywords)

#     return statements

# # ---------------------------
# # 4️⃣ Main
# # ---------------------------
# if __name__ == "__main__":
#     cik = "0000320193"  # Apple
#     year = 2025

#     print("Fetching 10-K filing from SEC...")
#     xbrl_model = fetch_10k_xbrl_model(cik, year)

#     print("Extracting hierarchical human-readable financial statements...")
#     statements = extract_hierarchical_statements_ixbrl(xbrl_model)

#     # Save as JSON
#     output_file = "financial_statements_human_labels.json"
#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(statements, f, indent=2, ensure_ascii=False)

#     print(f"✅ Done! Hierarchical human-readable statements saved to {output_file}")



# ############################## 5 ###################################


import requests
from arelle import Cntlr
from bs4 import BeautifulSoup
import json

# ---------------------------
# 1️⃣ Fetch 10-K XBRL/iXBRL filing from SEC
# ---------------------------
def fetch_10k_xbrl_model(cik: str, year: int):
    cik = str(cik).lstrip("0")
    headers = {"User-Agent": "Your Name contact@example.com"}

    # Get company submissions
    submissions_url = f"https://data.sec.gov/submissions/CIK{int(cik):010d}.json"
    resp = requests.get(submissions_url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    filings = data.get("filings", {}).get("recent", {})
    target_acc = None
    for form, acc_no, fdate in zip(filings["form"], filings["accessionNumber"], filings["filingDate"]):
        if form == "10-K" and fdate.startswith(str(year)):
            target_acc = acc_no
            break

    if not target_acc:
        raise RuntimeError(f"No 10-K filing found for CIK {cik} in {year}")

    acc_no_no_dashes = target_acc.replace("-", "")
    filing_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_no_no_dashes}/"

    resp = requests.get(filing_url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    xbrl_file_url = None
    for link in soup.find_all("a"):
        href = link.get("href", "")
        if href.endswith(".xml") and all(x not in href.lower() for x in ["cal", "def", "lab"]):
            xbrl_file_url = "https://www.sec.gov" + href if href.startswith("/") else filing_url + href
            break

    if not xbrl_file_url:
        raise RuntimeError("Could not find XBRL instance document.")

    cntlr = Cntlr.Cntlr(logFileName="logToPrint")
    xbrl_model = cntlr.modelManager.load(xbrl_file_url)
    if xbrl_model is None:
        raise RuntimeError("Failed to load XBRL instance into Arelle")

    return xbrl_model

# ---------------------------
# 2️⃣ Helper to get human-readable label
# ---------------------------
def get_label(fact):
    try:
        return fact.concept.label()  # iXBRL human-readable label
    except Exception:
        return fact.concept.qname.localName  # fallback to concept name

# ---------------------------
# 3️⃣ Ordered statement structures
# ---------------------------
BALANCE_SHEET_ORDER = [
    "Assets", [
        "CurrentAssets",
        "CashAndCashEquivalents",
        "AccountsReceivable",
        "Inventory",
        "OtherCurrentAssets",
        "NoncurrentAssets",
        "PropertyPlantAndEquipment",
        "IntangibleAssets",
        "Goodwill",
        "OtherNoncurrentAssets"
    ],
    "Liabilities", [
        "CurrentLiabilities",
        "AccountsPayable",
        "AccruedExpenses",
        "OtherCurrentLiabilities",
        "NoncurrentLiabilities",
        "LongTermDebt",
        "OtherNoncurrentLiabilities"
    ],
    "Equity", [
        "CommonStock",
        "AdditionalPaidInCapital",
        "RetainedEarnings",
        "TreasuryStock",
        "OtherEquity"
    ]
]

INCOME_STATEMENT_ORDER = [
    "Revenue",
    "CostOfRevenue",
    "GrossProfit",
    "OperatingExpenses",
    "SellingGeneralAdministrativeExpenses",
    "OperatingIncomeLoss",
    "OtherIncomeExpenses",
    "IncomeBeforeTax",
    "IncomeTaxExpenseBenefit",
    "NetIncomeLoss"
]

CASH_FLOW_STATEMENT_ORDER = [
    "OperatingActivities",
    "NetCashProvidedByUsedInOperatingActivities",
    "InvestingActivities",
    "NetCashProvidedByUsedInInvestingActivities",
    "FinancingActivities",
    "NetCashProvidedByUsedInFinancingActivities",
    "EffectOfExchangeRateChangesOnCash",
    "NetChangeInCash"
]

# ---------------------------
# 4️⃣ Recursive function to build ordered hierarchy
# ---------------------------
def build_ordered_hierarchy(facts, ordered_list):
    tree = {}
    for idx, item in enumerate(ordered_list):
        if isinstance(item, list):
            continue  # skip sublist itself

        # Find matching facts
        matching_facts = [f for f in facts if item.lower() in f.concept.qname.localName.lower() and f.isNumeric]

        # Check for nested sublist
        subtree = {}
        if idx + 1 < len(ordered_list) and isinstance(ordered_list[idx + 1], list):
            subtree = build_ordered_hierarchy(matching_facts, ordered_list[idx + 1])

        # Add remaining facts under this category
        for f in matching_facts:
            subtree[get_label(f)] = f.value

        if subtree:
            tree[item] = subtree

    return tree

# ---------------------------
# 5️⃣ Extract statements
# ---------------------------
def extract_ordered_statements_ixbrl(xbrl_model):
    statements = {
        "BalanceSheet": build_ordered_hierarchy(xbrl_model.facts, BALANCE_SHEET_ORDER),
        "IncomeStatement": build_ordered_hierarchy(xbrl_model.facts, INCOME_STATEMENT_ORDER),
        "CashFlowStatement": build_ordered_hierarchy(xbrl_model.facts, CASH_FLOW_STATEMENT_ORDER)
    }
    return statements

# ---------------------------
# 6️⃣ Main
# ---------------------------
if __name__ == "__main__":
    cik = "0000320193"  # Apple
    year = 2025

    print("Fetching 10-K filing from SEC...")
    xbrl_model = fetch_10k_xbrl_model(cik, year)

    print("Extracting hierarchical human-readable financial statements...")
    statements = extract_ordered_statements_ixbrl(xbrl_model)

    output_file = "financial_statements_ordered.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(statements, f, indent=2, ensure_ascii=False)

    print(f"✅ Done! Hierarchical statements with proper order saved to {output_file}")
