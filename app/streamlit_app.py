import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Setup source import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.topic_analyzer import TopicAnalyzer, get_insights

st.set_page_config(
    page_title="Customer Voice Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enterprise Dark Theme Styling - Zero Emojis
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .kpi-card {
        background: linear-gradient(135deg, #1e222d 0%, #151821 100%);
        border: 1px solid #2d3342;
        border-radius: 8px;
        padding: 18px 22px;
        margin-bottom: 15px;
    }
    .kpi-title {
        color: #8b949e;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .kpi-value {
        color: #ffffff;
        font-size: 2.1rem;
        font-weight: 700;
        line-height: 1.1;
    }
    .kpi-subtext {
        font-size: 0.8rem;
        color: #58a6ff;
        margin-top: 6px;
    }
    .badge-critical {
        background-color: #f85149;
        color: #ffffff;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.75rem;
    }
    .badge-positive {
        background-color: #2ea043;
        color: #ffffff;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_analyzer():
    return TopicAnalyzer()

analyzer = load_analyzer()

# Sidebar Control Center
with st.sidebar:
    st.markdown("## Customer Voice Intelligence")
    st.caption("Enterprise Aspect-Based Sentiment Analysis and Churn Risk Telemetry")
    st.markdown("---")

    data_source = st.radio(
        "Data Ingestion Source",
        options=["Benchmark Enterprise Reviews (20 records)", "Upload Custom CSV File"],
        index=0
    )

    df_reviews = None
    text_column = "review_text"

    if data_source == "Benchmark Enterprise Reviews (20 records)":
        benchmark_path = os.path.join(os.path.dirname(__file__), "..", "data", "amazon_reviews.csv")
        if os.path.exists(benchmark_path):
            df_reviews = pd.read_csv(benchmark_path)
            st.success(f"Benchmark dataset loaded ({len(df_reviews)} verified records).")
        else:
            st.error("Benchmark dataset file not found.")
    else:
        uploaded_file = st.file_uploader("Upload Reviews Dataset (CSV)", type=["csv"])
        if uploaded_file is not None:
            try:
                df_reviews = pd.read_csv(uploaded_file)
                st.success(f"Loaded {len(df_reviews):,} records.")
                candidate_cols = [c for c in df_reviews.columns if any(k in c.lower() for k in ["text", "review", "content", "feedback", "body"])]
                if candidate_cols:
                    text_column = st.selectbox("Select Review Text Column", options=df_reviews.columns, index=df_reviews.columns.get_loc(candidate_cols[0]))
                else:
                    text_column = st.selectbox("Select Review Text Column", options=df_reviews.columns)
            except Exception as e:
                st.error(f"Failed to read CSV: {e}")

    st.markdown("---")
    min_confidence = st.slider("Confidence Threshold", 0.50, 0.95, 0.65, 0.05)
    st.markdown("---")
    st.caption("Engine: ABSA Neural Lexicon v2.0 | Zero Emojis Enforced")

# Main Dashboard Header
st.title("Voice of Customer & Churn Risk Intelligence")
st.markdown("Automated classification of customer feedback across commercial aspects, defect identification, and escalation triage.")

if df_reviews is not None and text_column in df_reviews.columns:
    texts = df_reviews[text_column].dropna().astype(str).tolist()

    if not texts:
        st.warning("Selected column contains no valid text records.")
        st.stop()

    # Run Analysis
    with st.spinner("Executing aspect decomposition and risk telemetry..."):
        analysis_records = analyzer.analyze(texts)
        insights = get_insights(analysis_records)

    analysis_df = pd.DataFrame(analysis_records)

    # Attach original metadata if present
    for col in df_reviews.columns:
        if col not in analysis_df.columns and col != text_column and len(df_reviews) == len(analysis_df):
            analysis_df[col] = df_reviews[col].values

    # KPI Metrics Row
    total_count = insights.get("total_analyzed", 0)
    net_sentiment = insights.get("net_sentiment_score", 0.0)
    churn_rate = insights.get("churn_risk_percentage", 0.0)
    aspect_counts = insights.get("topic_distribution", {})
    top_aspect = max(aspect_counts, key=aspect_counts.get) if aspect_counts else "General"

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Ingested Reviews</div>
            <div class="kpi-value">{total_count:,}</div>
            <div class="kpi-subtext">Active telemetry window</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        sentiment_color = "#2ea043" if net_sentiment >= 0 else "#f85149"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Net Sentiment Score (NSS)</div>
            <div class="kpi-value" style="color: {sentiment_color};">{net_sentiment:+.1f}</div>
            <div class="kpi-subtext">Range: -100 to +100</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        risk_color = "#f85149" if churn_rate > 20 else "#58a6ff"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">High Churn Risk Ratio</div>
            <div class="kpi-value" style="color: {risk_color};">{churn_rate:.1f}%</div>
            <div class="kpi-subtext">Severe defect or cancellation signals</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Dominant Feedback Aspect</div>
            <div class="kpi-value" style="font-size: 1.5rem; padding-top: 6px;">{top_aspect}</div>
            <div class="kpi-subtext">Largest volume cluster</div>
        </div>
        """, unsafe_allow_html=True)

    # Tabs Layout
    tab_aspects, tab_escalations, tab_distributions, tab_explorer = st.tabs([
        "Aspect Analysis (ABSA)",
        "Escalation & Churn Triage",
        "Polarity Metrics",
        "Data Explorer & Export"
    ])

    with tab_aspects:
        st.subheader("Operational Aspect Breakdown")
        st.markdown("Feedback categorized into core commercial touchpoints with polarity attribution.")

        aspect_dict = insights.get("aspect_breakdown", {})
        if aspect_dict:
            aspect_summary_rows = []
            for aspect_name, stats in aspect_dict.items():
                aspect_summary_rows.append({
                    "Aspect": aspect_name,
                    "Total Mentions": stats["count"],
                    "Positive Reviews": stats["positive_count"],
                    "Negative Reviews": stats["negative_count"],
                    "Average Polarity": stats["avg_polarity"]
                })
            aspect_summary_df = pd.DataFrame(aspect_summary_rows).sort_values(by="Total Mentions", ascending=False)

            col_chart, col_table = st.columns([1.2, 1])
            with col_chart:
                fig_aspect = px.bar(
                    aspect_summary_df,
                    x="Aspect",
                    y="Total Mentions",
                    color="Average Polarity",
                    color_continuous_scale="RdBu",
                    range_color=[-1, 1],
                    title="Aspect Volume and Mean Polarity"
                )
                fig_aspect.update_layout(
                    plot_bgcolor="#161b22",
                    paper_bgcolor="#0e1117",
                    font=dict(color="#c9d1d9"),
                    xaxis=dict(gridcolor="#30363d"),
                    yaxis=dict(gridcolor="#30363d")
                )
                st.plotly_chart(fig_aspect, use_container_width=True)

            with col_table:
                st.markdown("#### Aspect Breakdown Table")
                st.dataframe(aspect_summary_df, use_container_width=True, hide_index=True)

    with tab_escalations:
        st.subheader("Escalation & Churn Risk Triage Queue")
        st.markdown("Automated ticket generation queue for customers demonstrating cancellation intent or severe hardware/service defects.")

        queue_items = insights.get("escalation_queue", [])
        if queue_items:
            queue_df = pd.DataFrame(queue_items)
            st.dataframe(
                queue_df,
                use_container_width=True,
                column_config={
                    "churn_risk_score": st.column_config.ProgressColumn(
                        "Churn Risk Index",
                        help="Calibrated risk severity (0-100)",
                        format="%d",
                        min_value=0,
                        max_value=100
                    ),
                    "review_id": "Ticket ID",
                    "aspect": "Aspect",
                    "sentiment": "Polarity",
                    "text": "Review Excerpt"
                },
                hide_index=True
            )

            # Export action
            json_export = queue_df.to_json(orient="records", indent=2)
            st.download_button(
                label="Export Triage Queue (JSON for Ticketing / Webhooks)",
                data=json_export,
                file_name="escalation_triage_queue.json",
                mime="application/json"
            )
        else:
            st.info("No critical churn escalation triggers detected in this dataset.")

    with tab_distributions:
        st.subheader("Sentiment Distribution and Keyword Drivers")
        col_dist1, col_dist2 = st.columns(2)

        with col_dist1:
            sent_dist = insights.get("sentiment_distribution", {})
            sent_df = pd.DataFrame(list(sent_dist.items()), columns=["Sentiment", "Count"])
            fig_pie = px.pie(
                sent_df,
                names="Sentiment",
                values="Count",
                color="Sentiment",
                color_discrete_map={"Positive": "#2ea043", "Negative": "#f85149", "Neutral": "#8b949e"},
                hole=0.45,
                title="Overall Sentiment Allocation"
            )
            fig_pie.update_layout(
                plot_bgcolor="#161b22",
                paper_bgcolor="#0e1117",
                font=dict(color="#c9d1d9")
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_dist2:
            key_drivers = insights.get("key_drivers", [])
            if key_drivers:
                driver_df = pd.DataFrame(key_drivers, columns=["Keyword", "Frequency"])
                fig_drivers = px.bar(
                    driver_df,
                    x="Frequency",
                    y="Keyword",
                    orientation="h",
                    title="Key Vocabulary Drivers",
                    color="Frequency",
                    color_continuous_scale="Blues"
                )
                fig_drivers.update_layout(
                    plot_bgcolor="#161b22",
                    paper_bgcolor="#0e1117",
                    font=dict(color="#c9d1d9"),
                    yaxis=dict(autorange="reversed")
                )
                st.plotly_chart(fig_drivers, use_container_width=True)

    with tab_explorer:
        st.subheader("Processed Review Explorer")
        filter_aspect = st.multiselect("Filter by Aspect", options=analysis_df["aspect"].unique(), default=list(analysis_df["aspect"].unique()))
        filter_sentiment = st.multiselect("Filter by Sentiment", options=analysis_df["sentiment"].unique(), default=list(analysis_df["sentiment"].unique()))

        filtered_df = analysis_df[
            (analysis_df["aspect"].isin(filter_aspect)) &
            (analysis_df["sentiment"].isin(filter_sentiment))
        ]

        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

        csv_download = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Processed Dataset (CSV)",
            data=csv_download,
            file_name="voc_processed_dataset.csv",
            mime="text/csv"
        )
else:
    st.info("Select or upload a dataset using the sidebar to begin analysis.")
