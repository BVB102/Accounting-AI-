import json
import urllib.request
import urllib.error

# STEP 1: Financial data
revenue = 100000
expenses = 65000

# STEP 2: Calculate financial results
net_income = revenue - expenses
profit_margin = (net_income / revenue) * 100

print("=== ACCOUNTING AI ASSISTANT ===")
print(f"Revenue: ${revenue:,.2f}")
print(f"Expenses: ${expenses:,.2f}")
print(f"Net Income: ${net_income:,.2f}")
print(f"Profit Margin: {profit_margin:.1f}%")

# STEP 3: Create the AI prompt
prompt = f"""
/no_think

You are an accounting assistant.

A company reports:
Revenue: ${revenue:,}
Expenses: ${expenses:,}
Net Income: ${net_income:,}
Net Profit Margin: {profit_margin:.1f}%

Explain these results in 3 short sentences.
Explain what the profit margin means.
Do not invent financial information.
Do not show your reasoning process.
"""

# STEP 4: Prepare the Ollama request
data = json.dumps({
    "model": "qwen3:4b-instruct",
    "prompt": prompt,
    "stream": True,
    "think": False,
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

# STEP 5: Connect to Ollama
print("\nConnecting to Ollama...", flush=True)

try:
    with urllib.request.urlopen(request, timeout=120) as response:
        print("\n=== AI FINANCIAL ANALYSIS ===\n", flush=True)

        for line in response:
            if not line.strip():
                continue

            result = json.loads(line.decode("utf-8"))

            if "error" in result:
                raise RuntimeError(result["error"])

            # Display generated text immediately
            answer = result.get("response", "")
            if answer:
                print(answer, end="", flush=True)

    print("\n\n=== ANALYSIS COMPLETE ===")

except urllib.error.URLError as error:
    print(f"\nConnection error: {error}")
    print("Check that Ollama is running on your Mac.")

except TimeoutError:
    print("\nOllama took too long to respond.")

except KeyboardInterrupt:
    print("\n\nAI generation stopped by user.")

except Exception as error:
    print(f"\nUnexpected error: {error}")
