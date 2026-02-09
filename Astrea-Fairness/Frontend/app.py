import streamlit as st
import pandas as pd
import requests
import io
import plotly.graph_objects as go
import plotly.express as px

BACKEND = "http://127.0.0.1:8000"

st.set_page_config(page_title="Astrea Fairness", layout="wide")
st.title("⚖️ Astrea Fairness Audit Platform")

# Select data type
data_type = st.radio(
    "Select Data Type:",
    ["Tabular", "Text", "Image", "Multimodal (Image-Caption Pairs)"],
    horizontal=True
)

# Common parameters
st.sidebar.header("Configuration")
sensitive = st.sidebar.text_input("Sensitive Attribute", "gender")
y_true = st.sidebar.text_input("Ground Truth Column", "hired")
y_pred = st.sidebar.text_input("Prediction Column", "hired")

# Data upload based on type
if data_type == "Tabular":
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    
    if uploaded_file:
        # Read file content once
        file_content = uploaded_file.read()
        
        # Prepare files for requests
        files = {"file": ("upload.csv", file_content)}
        params = {"sensitive": sensitive, "y_true": y_true, "y_pred": y_pred, "data_type": "tabular"}

        response = requests.post(f"{BACKEND}/audit-dataset/", files=files, params=params)
        
        if response.status_code == 200:
            result = response.json()
            
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📊 Audit Results",
                "📋 Detailed Metrics",
                "🔍 Bias Checks",
                "⚖️ Fairness Assessment",
                "📄 PDF Report"
            ])

            # ---------- TAB 1: OVERVIEW ----------
            with tab1:
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("📈 Fairness Score", f"{result['fairness_score']:.2%}")
                col2.metric("⚠️ Bias Level", result["bias_level"])
                col3.metric("👥 Dataset Size", result["dataset_size"])
                col4.metric("🔢 Groups Analyzed", len(result["group_distribution"]))

                # Group Distribution Visualization
                st.subheader("Group Distribution")
                group_data = result["group_distribution"]
                fig = go.Figure(data=[
                    go.Bar(x=list(group_data.keys()), y=list(group_data.values()), marker_color='indianred')
                ])
                fig.update_layout(title="Distribution of Sensitive Attribute", xaxis_title="Group", yaxis_title="Count")
                st.plotly_chart(fig, use_container_width=True)

                # Positive Rate by Group
                st.subheader("Selection Rate by Group")
                positive_rates = result.get("positive_rate_by_group", {})
                fig2 = go.Figure(data=[
                    go.Bar(x=list(positive_rates.keys()), y=list(positive_rates.values()), marker_color='lightblue')
                ])
                fig2.update_layout(
                    title="Positive Prediction Rate by Group (Higher is Better for All Groups)",
                    xaxis_title="Group",
                    yaxis_title="Positive Rate",
                    yaxis_range=[0, 1]
                )
                st.plotly_chart(fig2, use_container_width=True)

            # ---------- TAB 2: DETAILED METRICS ----------
            with tab2:
                st.subheader("Fairness Metrics Detailed View")
                
                metrics = result["metrics"]
                explanations = result.get("metrics_explanations", {})
                
                # Create a dashboard with metric cards
                col1, col2 = st.columns(2)
                
                metric_names = list(metrics.keys())
                for idx, metric_name in enumerate(metric_names):
                    if idx % 2 == 0:
                        col = col1
                    else:
                        col = col2
                    
                    with col:
                        with st.container():
                            st.markdown(f"### {metric_name.upper()}")
                            
                            metric_value = metrics[metric_name]
                            
                            # Color coding based on value
                            if metric_name == "dp_ratio":
                                color = "green" if metric_value >= 0.8 else "red"
                            else:
                                color = "green" if metric_value < 0.1 else ("yellow" if metric_value < 0.2 else "red")
                            
                            st.metric("Value", f"{metric_value:.4f}", delta=None)
                            
                            # Show explanation
                            if metric_name in explanations:
                                exp = explanations[metric_name]
                                with st.expander("📖 Learn More"):
                                    st.write(f"**Name:** {exp['name']}")
                                    st.write(f"**Description:** {exp['description']}")
                                    st.write(f"**Range:** {exp['range']}")
                                    st.write(f"**Impact:** {exp['impact']}")
                            
                            st.divider()
                
                # Metrics Visualization
                st.subheader("Metrics Overview (Line Chart)")
                metrics_df = pd.DataFrame({
                    "Metric": list(metrics.keys()),
                    "Value": list(metrics.values())
                })
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=metrics_df["Metric"],
                    y=metrics_df["Value"],
                    mode='lines+markers',
                    name='Metric Values',
                    line=dict(color='blue', width=2),
                    marker=dict(size=10)
                ))
                fig.update_layout(
                    title="All Fairness Metrics",
                    xaxis_title="Metric",
                    yaxis_title="Value",
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)

            # ---------- TAB 3: BIAS CHECKS ----------
            with tab3:
                st.subheader("🔍 Bias Detection Results")
                
                detailed_report = result.get("detailed_report", {})
                bias_checks = detailed_report.get("bias_checks", {})
                
                if bias_checks:
                    for check_name, check_result in bias_checks.items():
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            severity = check_result.get("severity", "unknown").upper()
                            
                            # Color based on severity
                            severity_colors = {
                                "NONE": "🟢",
                                "MINOR": "🟡",
                                "MODERATE": "🟠",
                                "SEVERE": "🔴"
                            }
                            
                            st.markdown(f"#### {severity_colors.get(severity, '⚪')} {check_name.replace('_', ' ').title()}")
                            st.write(check_result.get("description", ""))
                        
                        with col2:
                            st.metric("Value", f"{check_result.get('result', 0):.4f}")
                        
                        st.divider()
                else:
                    st.info("No detailed bias checks available")

            # ---------- TAB 4: FAIRNESS ASSESSMENT ----------
            with tab4:
                st.subheader("⚖️ Fairness Assessment")
                
                detailed_report = result.get("detailed_report", {})
                fairness_assessments = detailed_report.get("fairness_assessments", {})
                
                if fairness_assessments:
                    for assessment_name, assessment_result in fairness_assessments.items():
                        with st.container():
                            st.markdown(f"### {assessment_name.replace('_', ' ').title()}")
                            
                            if "status" in assessment_result:
                                status_color = "green" if "PASS" in assessment_result.get("status", "") else "red"
                                st.write(f"**Status:** {assessment_result['status']}")
                            
                            if "description" in assessment_result:
                                st.write(f"**Assessment:** {assessment_result['description']}")
                            
                            if "metrics" in assessment_result:
                                metrics_data = assessment_result["metrics"]
                                for metric_key, metric_val in metrics_data.items():
                                    st.write(f"- {metric_key}: {metric_val:.4f}")
                            
                            st.divider()
                
                # Recommendations
                st.subheader("📋 Recommendations")
                recommendations = detailed_report.get("recommendations", [])
                if recommendations:
                    for rec in recommendations:
                        severity_icon = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}
                        icon = severity_icon.get(rec.get("severity", ""), "⚪")
                        
                        with st.container():
                            st.markdown(f"#### {icon} {rec.get('issue', 'Issue')}")
                            st.write(f"**Severity:** {rec.get('severity', 'Unknown')}")
                            st.write(f"**Suggestion:** {rec.get('suggestion', '')}")
                            st.divider()
                else:
                    st.info("No recommendations available")

            # ---------- TAB 5: PDF REPORT ----------
            with tab5:
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
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

elif data_type == "Text":
    st.subheader("Text Bias Analysis")
    
    upload_option = st.radio("Upload method:", ["Upload TXT File", "Paste Text"])
    
    texts = []
    if upload_option == "Upload TXT File":
        uploaded_file = st.file_uploader("Upload Text File", type=["txt"])
        if uploaded_file:
            content = uploaded_file.read().decode('utf-8')
            # Split by lines or sentences
            texts = [line.strip() for line in content.split('\n') if line.strip()]
    else:
        text_input = st.text_area("Paste your text (one text per line):")
        if text_input:
            texts = [line.strip() for line in text_input.split('\n') if line.strip()]
    
    if texts:
        if st.button("Analyze Text for Bias"):
            with st.spinner("Analyzing text bias..."):
                try:
                    response = requests.post(
                        f"{BACKEND}/analyze-text/",
                        json={"texts": texts},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Check if error in response
                        if "error" in result:
                            st.error(f"❌ Backend Error: {result['error']}")
                        else:
                            # Display results in tabs
                            tab1, tab2, tab3, tab4 = st.tabs([
                                "📊 Overall Results", 
                                "👥 Gender Bias", 
                                "🌍 Race Bias", 
                                "😊 Sentiment Bias"
                            ])
                            
                            with tab1:
                                col1, col2, col3 = st.columns(3)
                                col1.metric("Overall Bias Score", f"{result.get('overall_text_bias_score', 0):.2%}")
                                col2.metric("Bias Level", result.get('bias_level', 'Unknown'))
                                col3.metric("Texts Analyzed", result.get('total_texts_analyzed', 0))
                            
                            with tab2:
                                gender = result.get('gender_analysis', {})
                                st.metric("Gender Bias Score", f"{gender.get('gender_bias_score', 0):.2%}")
                                st.write("**Gender Distribution:**")
                                gender_dist = gender.get('gender_percentages', {})
                                if gender_dist:
                                    st.bar_chart(gender_dist)
                                else:
                                    st.info("No gender data available")
                            
                            with tab3:
                                race = result.get('race_analysis', {})
                                st.metric("Race Bias Score", f"{race.get('race_bias_score', 0):.2%}")
                                st.write("**Race Distribution:**")
                                race_dist = race.get('race_percentages', {})
                                if race_dist:
                                    st.bar_chart(race_dist)
                                else:
                                    st.info("No race data available")
                            
                            with tab4:
                                sentiment = result.get('sentiment_analysis', {})
                                st.metric("Sentiment Bias Score", f"{sentiment.get('sentiment_bias_score', 0):.2%}")
                                st.write("**Sentiment Distribution:**")
                                sentiment_dist = sentiment.get('sentiment_percentages', {})
                                if sentiment_dist:
                                    st.bar_chart(sentiment_dist)
                                else:
                                    st.info("No sentiment data available")
                    else:
                        st.error(f"❌ HTTP Error {response.status_code}: {response.text}")
                except requests.exceptions.Timeout:
                    st.error("❌ Request timeout - backend is not responding. Make sure backend is running on http://127.0.0.1:8000")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

elif data_type == "Image":
    st.subheader("Image Dataset Bias Analysis")
    
    st.info("Upload images and provide demographic labels for each image")
    
    uploaded_files = st.file_uploader(
        "Upload image files", 
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.write(f"Uploaded {len(uploaded_files)} images")
        
        # Demographic labels
        demographic_input = st.text_area(
            "Enter demographic labels (one per line, in same order as images):",
            placeholder="e.g., male\nfemale\nmale\n..."
        )
        
        if demographic_input:
            demographics = [d.strip() for d in demographic_input.split('\n') if d.strip()]
            
            if len(demographics) == len(uploaded_files):
                if st.button("Analyze Images for Bias"):
                    with st.spinner("Analyzing image bias..."):
                        try:
                            # Prepare files for multipart request
                            files = {}
                            for i, f in enumerate(uploaded_files):
                                files[f"image_{i}"] = (f.name, f.read(), "image/jpeg")
                            
                            # Prepare query params
                            params = {
                                "demographics": str(demographics)
                            }
                            
                            response = requests.post(
                                f"{BACKEND}/analyze-images/",
                                files=files,
                                params=params,
                                timeout=30
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                
                                if "error" in result:
                                    st.error(f"❌ Backend Error: {result['error']}")
                                else:
                                    tab1, tab2, tab3 = st.tabs([
                                        "📊 Representation", 
                                        "🎨 Color Analysis", 
                                        "📸 Features"
                                    ])
                                    
                                    with tab1:
                                        rep = result.get('representation_analysis', {})
                                        st.metric("Demographic Parity Score", f"{rep.get('demographic_parity_score', 0):.2%}")
                                        st.write("**Group Distribution:**")
                                        group_dist = rep.get('group_percentages', {})
                                        if group_dist:
                                            st.bar_chart(group_dist)
                                        else:
                                            st.info("No group distribution data")
                                    
                                    with tab2:
                                        color = result.get('color_bias_analysis', {})
                                        st.write("**Color Profiles by Group:**")
                                        if 'color_profiles' in color:
                                            for group, profile in color['color_profiles'].items():
                                                st.write(f"**{group}:** R={profile.get('avg_red', 0):.2f}, G={profile.get('avg_green', 0):.2f}, B={profile.get('avg_blue', 0):.2f}")
                                        else:
                                            st.info("No color profile data")
                                    
                                    with tab3:
                                        st.write("**Image Bias Detection Complete**")
                                        st.metric("Overall Bias Score", f"{result.get('overall_image_bias_score', 0):.2%}")
                            else:
                                st.error(f"❌ HTTP Error {response.status_code}: {response.text}")
                        except requests.exceptions.Timeout:
                            st.error("❌ Request timeout - backend is not responding. Make sure backend is running.")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
            else:
                st.error(f"❌ Label count ({len(demographics)}) must match image count ({len(uploaded_files)})")
        else:
            st.info("Enter demographic labels to proceed")

elif data_type == "Multimodal (Image-Caption Pairs)":
    st.subheader("Multimodal Bias Analysis (Image-Caption Pairs)")
    
    st.info("Upload a CSV file with image paths/URLs and their captions, plus demographic labels")
    
    uploaded_file = st.file_uploader("Upload CSV with image-caption pairs", type=["csv"])
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("**File Preview:**")
            st.dataframe(df.head())
            
            col1, col2, col3 = st.columns(3)
            image_col = col1.selectbox("Image column:", df.columns)
            caption_col = col2.selectbox("Caption column:", df.columns)
            demo_col = col3.selectbox("Demographic column:", df.columns)
            
            if st.button("Analyze Multimodal Bias"):
                with st.spinner("Analyzing multimodal bias..."):
                    try:
                        data = {
                            "image_captions": df[[image_col, caption_col]].rename(
                                columns={image_col: "image", caption_col: "caption"}
                            ).to_dict(orient='records'),
                            "demographic_groups": df[demo_col].tolist()
                        }
                        
                        response = requests.post(
                            f"{BACKEND}/analyze-multimodal/",
                            json=data,
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            if "error" in result:
                                st.error(f"❌ Backend Error: {result['error']}")
                            else:
                                col1, col2, col3 = st.columns(3)
                                col1.metric("Overall Bias Score", f"{result.get('overall_multimodal_bias_score', 0):.2%}")
                                col2.metric("Bias Level", result.get('bias_level', 'Unknown'))
                                col3.metric("Pairs Analyzed", result.get('total_pairs_analyzed', 0))
                                
                                tab1, tab2, tab3 = st.tabs(["📐 Alignment", "👥 Representation", "🏷️ Attribution"])
                                
                                with tab1:
                                    align = result.get('alignment_analysis', {})
                                    st.metric("Alignment Score", f"{align.get('average_alignment_score', 0):.2%}")
                                    stereotype_count = align.get('stereotype_cases', 0)
                                    st.write(f"**Stereotype cases detected:** {stereotype_count}")
                                
                                with tab2:
                                    rep = result.get('representation_analysis', {})
                                    st.write("**Caption Length by Group:**")
                                    if 'group_representation_metrics' in rep:
                                        for group, metrics in rep['group_representation_metrics'].items():
                                            st.write(f"- **{group}:** {metrics.get('avg_caption_length', 0):.1f} words avg")
                                    else:
                                        st.info("No representation metrics available")
                                
                                with tab3:
                                    attr = result.get('attribution_analysis', {})
                                    st.write("**Attribution Bias by Group:**")
                                    if 'attribution_bias_by_group' in attr:
                                        for group, bias in attr['attribution_bias_by_group'].items():
                                            st.write(f"- **{group}:** {bias.get('combined_bias', 0):.2%}")
                                    else:
                                        st.info("No attribution data available")
                        else:
                            st.error(f"❌ HTTP Error {response.status_code}: {response.text}")
                    except requests.exceptions.Timeout:
                        st.error("❌ Request timeout - backend is not responding. Make sure backend is running.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error reading CSV: {str(e)}")
