import csv
import json
import urllib.request
from pathlib import Path

print("=== AI FINANCIAL ANALYZER ===\n")

# Find the CSV file in the same folder
file_path = Path(__file__).parent / "financial_data.csv"

# Read financial information
companies = []

with open(file_path, newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        name = row["Company"]
        revenue = float(row["Revenue"])
        expenses = float(row["Expenses"])

        net_income = revenue - expenses
        margin = net_income / revenue * 100 if revenue else 0

        companies.append({
            "name": name,
            "revenue": revenue,
            "expenses": expenses,
            "net_income": net_income,
            "margin": margin
        })

# Display calculations
for company in companies:
    print(f"Company: {company['name']}")
    print(f"Revenue: ${company['revenue']:,.2f}")
    print(f"Net Income: ${company['net_income']:,.2f}")
    print(f"Profit Margin: {company['margin']:.2f}%\n")

# Prepare financial results for AI
financial_results = json.dumps(companies, indent=2)

prompt = f"""
You are a financial analyst.

Analyze these fictional companies:

{financial_results}

Compare their profit margins.
Identify the company with the highest margin.
Identify the company with the lowest margin.
Explain your findings in four short sentences.
Use only the provided financial information.
"""

# Request analysis from Ollama
data = json.dumps({
    "model": "qwen3:4b-instruct",
    "prompt": prompt,
    "stream": True,
    "options": {
        "num_predict": 250,
        "temperature": 0.2
    }
}).encode("utf-8")

request = urllib.request.Request(
    "http://localhost:11434/api/generate",
    data=data,
    headers={"Content-Type": "application/json"}
)

print("=== AI COMPARISON ===\n", flush=True)

try:
    with urllib.request.urlopen(request, timeout=120) as response:
        for line in response:
            if not line.strip():
                continue

            result = json.loads(line.decode("utf-8"))
            print(result.get("response", ""), end="", flush=True)

    print("\n\n=== ANALYSIS COMPLETE ===")

except Exception as error:
    print(f"\nOllama error: {error}")
