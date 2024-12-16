# File path: mca_cash_flow_dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Initialize Streamlit app
st.title("Merchant Cash Advance (MCA) Underwriting Dashboard")

# File upload
uploaded_file = st.file_uploader("Upload a CSV/Excel file (Cash Flow Data)", type=["csv", "xlsx"])
if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file)
    
    st.write("### Uploaded Data")
    st.dataframe(data)

    # Sidebar inputs for MCA metrics
    st.sidebar.header("MCA Inputs")
    advance_amount = st.sidebar.number_input("Advance Amount ($)", min_value=1000, step=500, value=50000)
    retrieval_rate = st.sidebar.slider("Retrieval Rate (%)", 5.0, 30.0, 10.0, 0.1)
    factor_rate = st.sidebar.slider("Factor Rate", 1.0, 2.0, 1.2, 0.1)
    daily_revenue = st.sidebar.number_input("Daily Revenue ($)", min_value=100, step=50, value=1000)

    # Calculate MCA Metrics
    payback_amount = advance_amount * factor_rate
    daily_collections = daily_revenue * (retrieval_rate / 100)
    estimated_payback_period = payback_amount / daily_collections
    remaining_balance = [max(payback_amount - i * daily_collections, 0) for i in range(int(estimated_payback_period) + 1)]

    # Display Key Metrics
    st.write("### Key MCA Metrics")
    mca_metrics = {
        "Advance Amount ($)": advance_amount,
        "Factor Rate": factor_rate,
        "Total Payback Amount ($)": payback_amount,
        "Daily Collections ($)": daily_collections,
        "Estimated Payback Period (Days)": estimated_payback_period,
    }
    st.json(mca_metrics)

    # Add remaining balance chart
    st.write("### Remaining Balance Over Time")
    plt.figure(figsize=(10, 5))
    plt.plot(range(len(remaining_balance)), remaining_balance, label="Remaining Balance")
    plt.axhline(y=0, color='r', linestyle='--', label="Payback Complete")
    plt.xlabel("Days")
    plt.ylabel("Remaining Balance ($)")
    plt.legend()
    st.pyplot(plt)

    # Export adjusted data
    st.write("### Export Adjusted Data")
    mca_data = pd.DataFrame({
        "Day": range(len(remaining_balance)),
        "Remaining Balance": remaining_balance
    })
    csv = mca_data.to_csv(index=False)
    st.download_button("Download Remaining Balance Data", csv, "remaining_balance.csv", "text/csv")

else:
    st.info("Please upload a cash flow file to proceed.")

# Footer
st.write("---")
st.write("Developed with 💻 using Streamlit")

# Deployment instructions
st.sidebar.title("Deployment")
st.sidebar.write("""
To deploy this dashboard:
1. Save this file as `mca_cash_flow_dashboard.py`.
2. Create a `requirements.txt` file with the following:
    - pandas
    - streamlit
    - matplotlib
3. Deploy to [Streamlit Cloud](https://streamlit.io/cloud).
""")
