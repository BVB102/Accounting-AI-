import streamlit as st
import json
import urllib.request

st.set_page_config(
    page_title="Accounting AI",
    page_icon="📊",
    layout="centered"
)

st.title("Accounting AI Assistant")
st.write("Analyze financial results using local AI.")

# Financial inputs
revenue = st.number_input(
    "Revenue ($)",
    min_value=0.0,
    value=100000.0,
    step=1000.0
)

expenses = st.number_input(
    "Expenses ($)",
    min_value=0.0,
    value=65000.0,
    step=1000.0
)

# Calculate financial results
net_income = revenue - expenses
margin = (net_income / revenue * 100) if revenue > 0 else 0

# Display results
col1, col2 = st.columns(2)

with col1:
    st.metric("Net Income", f"${net_income:,.2f}")

with col2:
    st.metric("Profit Margin", f"{margin:.2f}%")

# AI analysis
if st.button("Analyze with AI"):

    if revenue == 0:
        st.error("Revenue must be greater than zero.")
    else:
        prompt = f"""
        You are an accounting assistant.
        Explain these financial results in 3 short sentences.

        Revenue: ${revenue:,.2f}
        Expenses: ${expenses:,.2f}
        Net Income: ${net_income:,.2f}
        Profit Margin: {margin:.2f}%

        Do not invent additional information.
        """

        data = json.dumps({
            "model": "qwen3:4b-instruct",
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 200,
                "temperature": 0.2
            }
        }).encode("utf-8")

        request = urllib.request.Request(
            "http://localhost:11434/api/generate",
            data=data,
            headers={"Content-Type": "application/json"}
        )

        with st.spinner("Analyzing with local AI..."):
            try:
                with urllib.request.urlopen(
                    request, timeout=120
                ) as response:
                    result = json.load(response)

                st.subheader("AI Financial Analysis")
                st.write(result["response"])

            except Exception as error:
                st.error(f"Ollama connection error: {error}")
