
import json
import urllib.request
import urllib.error

print("=== ACCOUNTING AI ASSISTANT ===")

# Ask the user for financial data
try:
    revenue = float(input("Enter revenue: $").replace(",", ""))
    expenses = float(input("Enter expenses: $").replace(",", ""))

    if revenue <= 0:
        raise ValueError("Revenue must be greater than zero.")

    if expenses < 0:
        raise ValueError("Expenses cannot be negative.")

except ValueError as error:
    print("Invalid input:", error)
    raise SystemExit(1)

# Calculate results
net_income = revenue - expenses
profit_margin = net_income / revenue * 100

print(f"\nRevenue: ${revenue:,.2f}")
print(f"Expenses: ${expenses:,.2f}")
print(f"Net Income: ${net_income:,.2f}")
print(f"Net Profit Margin: {profit_margin:.1f}%")

# Prepare the AI prompt
prompt = f"""
You are an accounting assistant.

Revenue: ${revenue:,.2f}
Expenses: ${expenses:,.2f}
Net income: ${net_income:,.2f}
Net profit margin: {profit_margin:.1f}%

Explain these financial results in three short sentences.
Explain what the profit margin means.
Do not invent additional information.
"""

# Send results to Ollama
data = json.dumps({
    "model": "qwen3:4b-instruct",
    "prompt": prompt,
    "stream": True,
    "options": {
        "num_predict": 200,
        "temperature": 0.2
    }
}).encode("utf-8")

request = urllib.request.Request(
    "http://localhost:11434/api/generate",
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

print("\nConnecting to Ollama...", flush=True)

try:
    with urllib.request.urlopen(request, timeout=120) as response:
        print("\n=== AI FINANCIAL ANALYSIS ===\n")

        for line in response:
            if not line.strip():
                continue

            result = json.loads(line.decode("utf-8"))

            if "error" in result:
                raise RuntimeError(result["error"])

            print(result.get("response", ""), end="", flush=True)

    print("\n\n=== ANALYSIS COMPLETE ===")

except urllib.error.URLError as error:
    print("\nConnection error:", error)
    print("Check that Ollama is running.")

except KeyboardInterrupt:
    print("\nAI generation stopped.")
