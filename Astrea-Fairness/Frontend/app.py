import streamlit as st
import pandas as pd
import requests

BACKEND = "http://127.0.0.1:8000"

st.set_page_config(page_title="Astrea Fairness", layout="wide")
st.title("⚖️ Astrea Fairness Audit Platform")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

sensitive = st.text_input("Sensitive Attribute", "gender")
y_true = st.text_input("Ground Truth Column", "hired")
y_pred = st.text_input("Prediction Column", "hired")

if uploaded_file:
    # Read file content once
    file_content = uploaded_file.read()
    
    # Prepare files for requests
    files = {"file": ("upload.csv", file_content)}
    params = {"sensitive": sensitive, "y_true": y_true, "y_pred": y_pred}

    response = requests.post(f"{BACKEND}/audit-dataset/", files=files, params=params)
    result = response.json()

    tab1, tab2, tab3 = st.tabs(["📊 Audit Results", "📄 PDF Report", "🛠️ How to Fix Bias"])

    # ---------- TAB 1 ----------
    with tab1:
        st.metric("Fairness Score", result["fairness_score"])
        st.metric("Bias Level", result["bias_level"])

        st.subheader("Fairness Metrics")
        st.dataframe(pd.DataFrame.from_dict(result["metrics"], orient="index", columns=["Value"]))

        st.subheader("Group Distribution")
        st.bar_chart(result["group_distribution"])

    # ---------- TAB 2 ----------
    with tab2:
        st.info("Generate a full PDF fairness audit report")

        pdf = requests.post(
            f"{BACKEND}/audit-dataset/pdf",
            files=files,
            params=params
        )

        # Check if request was successful
        if pdf.status_code == 200 and pdf.headers.get('content-type') == 'application/pdf':
            st.download_button(
                "⬇️ Download PDF Report",
                data=pdf.content,
                file_name="fairness_audit_report.pdf",
                mime="application/pdf"
            )
        else:
            try:
                error_msg = pdf.json().get('error', 'Unknown error occurred')
            except:
                error_msg = f"Error: HTTP {pdf.status_code}"
            st.error(f"❌ Failed to generate PDF: {error_msg}")

    # ---------- TAB 3 ----------
    with tab3:
        st.subheader("Bias Mitigation Recommendations")

        for rec in result["mitigation"]:
            st.warning(f"**{rec['issue']}**")
            st.write(rec["fix"])
