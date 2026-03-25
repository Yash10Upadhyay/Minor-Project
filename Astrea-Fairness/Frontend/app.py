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
# configuration inputs placed on main page for simplicity
st.write("### Configuration")
sensitive = st.text_input("Sensitive Attribute", "gender")
y_true = st.text_input("Ground Truth Column", "hired")
y_pred = st.text_input("Prediction Column", "hired")

# Data upload based on type
if data_type == "Tabular":
    with st.expander("📖 How to use Tabular Analysis", expanded=False):
        st.markdown("""
        ### **Tabular Data Analysis Guide**
        
        **What it analyzes:** Hiring decisions, loan approvals, performance ratings, and other structured data.
        
          **Required Steps:**
          1. Upload a CSV file with your data
          2. (The system will automatically audit the **gender** column if present;
              no need to change the sensitive attribute field unless you really want to.)
          3. Specify **Ground Truth Column** (actual outcome)
          4. Specify **Prediction Column** (predicted outcome)
          5. View results in 5 tabs
        
        **Example CSV Format:**
        ```
        gender,age,hired,predicted_hired
        male,35,yes,yes
        female,32,no,no
        male,28,yes,yes
        ```
        
        **What You'll See:**
        - 📊 Audit Results - Overview metrics
        - 📋 Detailed Metrics - All fairness metrics
        - 🔍 Bias Checks - Specific bias detection
        - ⚖️ Fairness Assessment - Pass/fail results
        - 📄 PDF Report - Download complete audit
        """)
    
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
    st.subheader("📝 Text Bias Analysis")
    
    with st.expander("📖 How to use Text Analysis", expanded=False):
        st.markdown("""
        ### **Text Data Analysis Guide**
        
        **What it analyzes:** Gender bias, race bias, and sentiment bias in text like resumes, descriptions, and reviews.
        
        **Steps:**
        1. Choose upload method: File or Paste
        2. Upload TXT file OR paste text directly
        3. Each line = one text to analyze
        4. Click "Analyze Text for Bias"
        5. View 4 analysis tabs
        
        **Example Texts:**
        ```
        The ambitious businessman led the team with authority
        The friendly woman helped organize the office schedule
        An intelligent engineer solved complex problems
        ```
        
        **What You'll See:**
        - 📊 Overall Results - Bias score and level
        - 👥 Gender Bias - Masculine vs feminine language patterns
        - 🌍 Race Bias - Racial stereotype detection
        - 😊 Sentiment Bias - Emotional language patterns
        """)
    
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
    st.subheader("🖼️ Image Dataset Bias Analysis")
    
    with st.expander("📖 How to use Image Analysis", expanded=False):
        st.markdown("""
        ### **Image Data Analysis Guide**
        
        **What it analyzes:** 9 different bias dimensions including demographics, race, age, skin tone, pose, background, clothing, and emotion.
        
        **Steps:**
        1. Upload multiple images (JPG/PNG)
        2. Enter demographic labels (one per image)
        3. Click "🔍 Analyze Images for Bias"
        4. View 9 detailed analysis tabs
        
        **Example Labels (the demo concentrates on ethnicity/race):**
        ```
        male
        female
        male
        young
        adult
        ```
        
        **You Can Use Any Labels, but race/ethnicity is the focus:**
        - Race/ethnicity: asian, caucasian, african, hispanic, etc.
        - (other labels are ignored in this simplified demo)
        
        **9 Analyses You'll See:**
        1. 👥 Demographic Representation
        2. 🌍 Race/Ethnicity Distribution
        3. 👤 Gender Balance
        4. 👶 Age Groups
        5. 🎨 Skin Tone Diversity
        6. 🎭 Pose & Body Composition
        7. 🏞️ Background Context
        8. 🧥 Clothing & Accessories
        9. 😊 Emotion & Expression
        """)
    
    st.info("Upload images and provide demographic labels (e.g., male, female, young, adult)")
    
    uploaded_files = st.file_uploader(
        "Upload image files", 
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.write(f"✅ Uploaded {len(uploaded_files)} images")
        
        # Demographic labels
        demographic_input = st.text_area(
            "Enter demographic labels (one per line, in same order as images):",
            placeholder="Examples:\nmale\nfemale\nmale\nyoung\nadult\n\nOr use custom labels"
        )
        
        if demographic_input:
            demographics = [d.strip() for d in demographic_input.split('\n') if d.strip()]
            
            if len(demographics) == len(uploaded_files):
                if st.button("🔍 Analyze Images for Bias", key="analyze_images"):
                    with st.spinner("⏳ Analyzing images across 8 dimensions..."):
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
                                timeout=60
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                
                                if "error" in result:
                                    st.error(f"❌ Backend Error: {result['error']}")
                                else:
                                    # Display overall score first
                                    col1, col2, col3, col4 = st.columns(4)
                                    col1.metric("📈 Overall Bias Score", f"{result.get('overall_image_bias_score', 0):.2%}")
                                    col2.metric("⚠️ Bias Level", result.get('bias_level', 'Unknown'))
                                    col3.metric("🖼️ Images Analyzed", result.get('total_images_analyzed', 0))
                                    
                                    # Bias Summary
                                    bias_summary = result.get('bias_summary', {})
                                    col4.metric("🚨 Critical Issues", int(bias_summary.get('critical_issues', 0)))
                                    
                                    st.divider()
                                    
                                    # Create tabs for each analysis type
                                    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
                                        "👥 Demographics",
                                        "🌍 Race/Ethnicity",
                                        "👤 Gender",
                                        "👶 Age Groups",
                                        "🎨 Skin Tone",
                                        "🎭 Pose & Body",
                                        "🏞️ Background",
                                        "🧥 Clothing",
                                        "😊 Emotion"
                                    ])
                                    
                                    # Tab 1: Demographic Representation
                                    with tab1:
                                        st.subheader("Demographic Representation")
                                        rep = result.get('demographic_representation', {})
                                        
                                        if rep:
                                            col1, col2 = st.columns(2)
                                            
                                            with col1:
                                                st.metric("Demographic Parity Score", f"{rep.get('demographic_parity_score', 0):.2%}")
                                                st.metric("Disparity Ratio", f"{rep.get('representation_disparity_ratio', 1):.2f}x")
                                                st.metric("Imbalance Detected", "🔴 Yes" if rep.get('imbalance_detected') else "🟢 No")
                                            
                                            with col2:
                                                group_dist = rep.get('group_percentages', {})
                                                if group_dist:
                                                    fig = go.Figure(data=[
                                                        go.Bar(x=list(group_dist.keys()), y=list(group_dist.values()), marker_color='steelblue')
                                                    ])
                                                    fig.update_layout(title="Group Distribution (%)", xaxis_title="Group", yaxis_title="Percentage (%)")
                                                    st.plotly_chart(fig, use_container_width=True)
                                                else:
                                                    st.info("No group distribution data")
                                    
                                    # Tab 2: Race/Ethnicity
                                    with tab2:
                                        st.subheader("Race/Ethnicity Analysis")
                                        race = result.get('race_ethnicity_analysis', {})
                                        
                                        if race:
                                            col1, col2 = st.columns(2)
                                            
                                            with col1:
                                                st.metric("Race Bias Detected", "🔴 Yes" if race.get('race_bias_detected') else "🟢 No")
                                                st.metric("Representation Disparity", f"{race.get('race_representation_disparity', 1):.2f}x")
                                            
                                            with col2:
                                                race_pct = race.get('race_percentages', {})
                                                if race_pct:
                                                    fig = go.Figure(data=[
                                                        go.Pie(labels=list(race_pct.keys()), values=list(race_pct.values()), title="Race/Ethnicity Distribution")
                                                    ])
                                                    st.plotly_chart(fig, use_container_width=True)
                                                else:
                                                    st.info("No race data available")
                                    
                                    # Tab 3: Gender
                                    with tab3:
                                        st.subheader("Gender Representation")
                                        gender = result.get('gender_analysis', {})
                                        
                                        if gender:
                                            col1, col2 = st.columns(2)
                                            
                                            with col1:
                                                st.metric("Gender Imbalance Detected", "🔴 Yes" if gender.get('gender_imbalance_detected') else "🟢 No")
                                                st.metric("Gender Disparity Ratio", f"{gender.get('gender_disparity_ratio', 1):.2f}x")
                                            
                                            with col2:
                                                gender_pct = gender.get('gender_percentages', {})
                                                if gender_pct:
                                                    fig = go.Figure(data=[
                                                        go.Bar(x=list(gender_pct.keys()), y=list(gender_pct.values()), marker_color='lightcoral')
                                                    ])
                                                    fig.update_layout(title="Gender Distribution (%)", xaxis_title="Gender", yaxis_title="Percentage (%)")
                                                    st.plotly_chart(fig, use_container_width=True)
                                    
                                    # Tab 4: Age Groups
                                    with tab4:
                                        st.subheader("Age Group Analysis")
                                        age = result.get('age_group_analysis', {})
                                        
                                        if age:
                                            col1, col2 = st.columns(2)
                                            
                                            with col1:
                                                st.metric("Age Bias Detected", "🔴 Yes" if age.get('age_representation_bias_detected') else "🟢 No")
                                            
                                            with col2:
                                                age_pct = age.get('age_percentages', {})
                                                if age_pct:
                                                    fig = go.Figure(data=[
                                                        go.Bar(x=list(age_pct.keys()), y=list(age_pct.values()), marker_color='mediumpurple')
                                                    ])
                                                    fig.update_layout(title="Age Group Distribution (%)", xaxis_title="Age Group", yaxis_title="Percentage (%)")
                                                    st.plotly_chart(fig, use_container_width=True)
                                    
                                    # Tab 5: Skin Tone
                                    with tab5:
                                        st.subheader("Skin Tone Diversity Analysis")
                                        skin = result.get('skin_tone_analysis', {})
                                        
                                        if skin:
                                            col1, col2 = st.columns(2)
                                            
                                            with col1:
                                                st.metric("Skin Tone Bias Detected", "🔴 Yes" if skin.get('skin_tone_bias_detected') else "🟢 No")
                                                st.metric("Tone Diversity Score", f"{skin.get('skin_tone_diversity_score', 0):.2%}")
                                            
                                            with col2:
                                                skin_pct = skin.get('skin_tone_percentages', {})
                                                if skin_pct:
                                                    fig = go.Figure(data=[
                                                        go.Bar(x=list(skin_pct.keys()), y=list(skin_pct.values()), marker_color='goldenrod')
                                                    ])
                                                    fig.update_layout(title="Skin Tone Distribution (%)", xaxis_title="Tone", yaxis_title="Percentage (%)")
                                                    st.plotly_chart(fig, use_container_width=True)
                                            
                                            # By demographic breakdown
                                            st.write("**Skin Tone Distribution by Demographic Group:**")
                                            skin_by_demo = skin.get('skin_tone_by_demographic', {})
                                            if skin_by_demo:
                                                for demo_group, tone_data in skin_by_demo.items():
                                                    st.write(f"- **{demo_group}:** {dict(tone_data)}")
                                    
                                    # Tab 6: Pose & Body Composition
                                    with tab6:
                                        st.subheader("Pose & Body Composition Analysis")
                                        pose = result.get('pose_composition_analysis', {})
                                        
                                        if pose:
                                            col1, col2 = st.columns(2)
                                            
                                            with col1:
                                                st.metric("Pose Bias Detected", "🔴 Yes" if pose.get('pose_bias_detected') else "🟢 No")
                                                st.metric("Pose Diversity Score", f"{pose.get('pose_diversity_score', 0):.2%}")
                                            
                                            with col2:
                                                pose_pct = pose.get('pose_percentages', {})
                                                if pose_pct:
                                                    fig = go.Figure(data=[
                                                        go.Bar(x=list(pose_pct.keys()), y=list(pose_pct.values()), marker_color='lightseagreen')
                                                    ])
                                                    fig.update_layout(title="Pose Distribution (%)", xaxis_title="Pose Type", yaxis_title="Percentage (%)")
                                                    st.plotly_chart(fig, use_container_width=True)
                                            
                                            st.write("**Pose by Demographic Group:**")
                                            pose_by_demo = pose.get('pose_by_demographic', {})
                                            if pose_by_demo:
                                                for demo_group, pose_data in pose_by_demo.items():
                                                    st.write(f"- **{demo_group}:** {dict(pose_data)}")
                                    
                                    # Tab 7: Background Context
                                    with tab7:
                                        st.subheader("Background & Context Analysis")
                                        bg = result.get('background_context_analysis', {})
                                        
                                        if bg:
                                            col1, col2 = st.columns(2)
                                            
                                            with col1:
                                                st.metric("Background Bias Detected", "🔴 Yes" if bg.get('background_bias_detected') else "🟢 No")
                                                st.metric("Background Diversity", f"{bg.get('background_diversity', 0):.2%}")
                                            
                                            with col2:
                                                bg_pct = bg.get('background_percentages', {})
                                                if bg_pct:
                                                    fig = go.Figure(data=[
                                                        go.Bar(x=list(bg_pct.keys()), y=list(bg_pct.values()), marker_color='paleturquoise')
                                                    ])
                                                    fig.update_layout(title="Background Distribution (%)", xaxis_title="Background Type", yaxis_title="Percentage (%)")
                                                    st.plotly_chart(fig, use_container_width=True)
                                            
                                            st.write("**Background by Demographic Group:**")
                                            bg_by_demo = bg.get('background_by_demographic', {})
                                            if bg_by_demo:
                                                for demo_group, bg_data in bg_by_demo.items():
                                                    st.write(f"- **{demo_group}:** {dict(bg_data)}")
                                    
                                    # Tab 8: Clothing & Accessories
                                    with tab8:
                                        st.subheader("Clothing & Accessories Analysis")
                                        clothing = result.get('clothing_accessories_analysis', {})
                                        
                                        if clothing:
                                            col1, col2 = st.columns(2)
                                            
                                            with col1:
                                                st.metric("Clothing Bias Detected", "🔴 Yes" if clothing.get('clothing_bias_detected') else "🟢 No")
                                                st.metric("Style Diversity", f"{clothing.get('clothing_style_diversity', 0):.2%}")
                                            
                                            with col2:
                                                cloth_pct = clothing.get('clothing_percentages', {})
                                                if cloth_pct:
                                                    fig = go.Figure(data=[
                                                        go.Bar(x=list(cloth_pct.keys()), y=list(cloth_pct.values()), marker_color='plum')
                                                    ])
                                                    fig.update_layout(title="Clothing Style Distribution (%)", xaxis_title="Style", yaxis_title="Percentage (%)")
                                                    st.plotly_chart(fig, use_container_width=True)
                                            
                                            st.write("**Clothing by Demographic Group:**")
                                            cloth_by_demo = clothing.get('clothing_by_demographic', {})
                                            if cloth_by_demo:
                                                for demo_group, cloth_data in cloth_by_demo.items():
                                                    st.write(f"- **{demo_group}:** {dict(cloth_data)}")
                                    
                                    # Tab 9: Emotion & Expression
                                    with tab9:
                                        st.subheader("Emotion & Expression Analysis")
                                        emotion = result.get('emotion_expression_analysis', {})
                                        
                                        if emotion:
                                            col1, col2 = st.columns(2)
                                            
                                            with col1:
                                                st.metric("Emotion Bias Detected", "🔴 Yes" if emotion.get('emotion_bias_detected') else "🟢 No")
                                                st.metric("Emotion Diversity", f"{emotion.get('emotion_diversity', 0):.2%}")
                                            
                                            with col2:
                                                emotion_pct = emotion.get('emotion_percentages', {})
                                                if emotion_pct:
                                                    fig = go.Figure(data=[
                                                        go.Bar(x=list(emotion_pct.keys()), y=list(emotion_pct.values()), marker_color='salmon')
                                                    ])
                                                    fig.update_layout(title="Emotion Distribution (%)", xaxis_title="Emotion", yaxis_title="Percentage (%)")
                                                    st.plotly_chart(fig, use_container_width=True)
                                            
                                            st.write("**Emotion by Demographic Group:**")
                                            emotion_by_demo = emotion.get('emotion_by_demographic', {})
                                            if emotion_by_demo:
                                                for demo_group, emotion_data in emotion_by_demo.items():
                                                    st.write(f"- **{demo_group}:** {dict(emotion_data)}")
                                    
                                    # Summary Section
                                    st.divider()
                                    st.subheader("📋 Bias Summary")
                                    col1, col2, col3 = st.columns(3)
                                    col1.metric("🔴 Critical Issues", int(bias_summary.get('critical_issues', 0)))
                                    col2.metric("🟠 Moderate Issues", int(bias_summary.get('moderate_issues', 0)))
                                    col3.metric("🟡 Minor Issues", int(bias_summary.get('minor_issues', 0)))
                                    
                            else:
                                st.error(f"❌ HTTP Error {response.status_code}: {response.text}")
                        except requests.exceptions.Timeout:
                            st.error("❌ Request timeout - backend is not responding. Ensure backend is running on http://127.0.0.1:8000")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
            else:
                st.error(f"❌ Label count ({len(demographics)}) must match image count ({len(uploaded_files)})")
                st.info(f"Please provide exactly {len(uploaded_files)} labels")
        else:
            st.info("👆 Enter demographic labels above to proceed")


elif data_type == "Multimodal (Image-Caption Pairs)":
    st.subheader("Multimodal Bias Analysis (Image-Caption Pairs)")
    
    with st.expander("📖 How to use Multimodal Analysis", expanded=False):
        st.markdown("""
        ### **Multimodal Data Analysis Guide**
        
        **What it analyzes:** Image-caption alignment, stereotype presence in descriptions, and attribute associations.
        
        **Required CSV Columns:**
        - `image_path` - Path to image file
        - `caption` - Text description of image
        - `demographic_group` - Group label
        
        **Steps:**
        1. Create/prepare CSV with 3 columns
        2. Upload the CSV file
        3. Select appropriate column names
        4. Click "Analyze Multimodal Bias"
        5. View 3 analysis tabs
        
        **Example CSV Format:**
        ```
        image_path,caption,demographic_group
        img_001.jpg,A brilliant engineer solving problems,male
        img_002.jpg,A friendly woman helping colleagues,female
        img_003.jpg,A powerful executive making decisions,male
        ```
        
        **What You'll See:**
        - 📐 Alignment Analysis - Caption-image quality alignment
        - 👥 Representation - Description consistency across groups
        - 🏷️ Attribution - Stereotype detection in captions
        """)
    
    st.info("Upload a CSV file with image paths/URLs, captions, and demographic labels")
    
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
