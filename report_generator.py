import csv
from pathlib import Path

# Find the project folder
folder = Path(__file__).parent

input_file = folder / "financial_data.csv"
output_file = folder / "financial_report.csv"

# Read financial data and calculate results
with open(input_file, newline="") as file:
    reader = csv.DictReader(file)
    companies = list(reader)

if not companies:
    print("Error: No financial data found.")
    raise SystemExit(1)

with open(output_file, "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Company",
        "Revenue",
        "Expenses",
        "Net Income",
        "Profit Margin (%)"
    ])

    for company in companies:
        revenue = float(company["Revenue"])
        expenses = float(company["Expenses"])

        net_income = revenue - expenses
        margin = net_income / revenue * 100 if revenue else 0

        writer.writerow([
            company["Company"],
            revenue,
            expenses,
            net_income,
            round(margin, 2)
        ])

print("Financial report created successfully!")
print("File: financial_report.csv")
