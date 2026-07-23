import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import os

import sys

# Add parent directory to path to import src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.topic_analyzer import TopicAnalyzer, get_insights

@st.cache_resource
def load_analyzer():
    return TopicAnalyzer()

# Setup Page
st.set_page_config(page_title="Review Intelligence", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Aesthetic UI
st.markdown("""
<style>
    .reportview-container .main .block-container{
        padding-top: 2rem;
    }
    .kpi-card {
        background-color: #262730;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 5px solid #00B4D8;
    }
    .kpi-title {
        color: #9a9a9a;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .kpi-value {
        color: #ffffff;
        font-size: 2rem;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #262730;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00B4D8 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/brain.png", width=60)
    st.title("Review Intelligence")
    st.markdown("Transform raw customer reviews into actionable product insights using advanced NLP.")
    st.divider()

    st.markdown("### 📥 Data Ingestion")
    uploaded_file = st.file_uploader("Upload Reviews (CSV)", type=["csv"], help="CSV must contain a 'review_text' column.")

    st.divider()
    st.caption("Powered by DistilBERT & BERTopic")

# Main Header
st.title("📊 NLP Review Intelligence Dashboard")
st.markdown("Automate sentiment classification and topic discovery to prioritize product improvements.")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        if 'review_text' not in df.columns:
            st.error("Error: CSV must contain a 'review_text' column.")
            st.stop()

        st.success(f"Successfully loaded {len(df):,} reviews.")

        if st.button("🚀 Run AI Analysis", use_container_width=True):
            with st.spinner("Extracting insights using deep learning models..."):
                texts = df['review_text'].dropna().tolist()

                try:
                    analyzer = load_analyzer()
                    analysis_results = analyzer.analyze(texts)
                    insights = get_insights(analysis_results)
                    result = {
                        "analysis": analysis_results,
                        "insights": insights
                    }

                    st.divider()

                    # --- KPI Metrics Row ---
                    st.markdown("### 🎯 Executive Summary")
                    total_reviews = result['insights']['total_analyzed']
                    topic_dist = result['insights']['topic_distribution']
                    sentiment_dist = result['insights']['sentiment_distribution']

                    pos_pct = (sentiment_dist.get('Positive', 0) / total_reviews) * 100 if total_reviews > 0 else 0
                    neg_pct = (sentiment_dist.get('Negative', 0) / total_reviews) * 100 if total_reviews > 0 else 0

                    # Find top topic (excluding General/None if possible, here just the highest count)
                    top_topic = max(topic_dist, key=topic_dist.get) if topic_dist else "N/A"

                    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

                    kpi1.markdown(f'<div class="kpi-card"><div class="kpi-title">Total Analyzed</div><div class="kpi-value">{total_reviews:,}</div></div>', unsafe_allow_html=True)
                    kpi2.markdown(f'<div class="kpi-card"><div class="kpi-title">Positive Sentiment</div><div class="kpi-value">{pos_pct:.1f}%</div></div>', unsafe_allow_html=True)
                    kpi3.markdown(f'<div class="kpi-card"><div class="kpi-title">Critical Complaints</div><div class="kpi-value">{neg_pct:.1f}%</div></div>', unsafe_allow_html=True)
                    kpi4.markdown(f'<div class="kpi-card"><div class="kpi-title">Primary Topic</div><div class="kpi-value">{top_topic}</div></div>', unsafe_allow_html=True)

                    st.write("") # Spacing

                    # --- Tabbed Views ---
                    tab1, tab2, tab3 = st.tabs(["📈 Sentiment Analysis", "🧩 Topic Modeling", "🔍 Raw Data Explorer"])

                    with tab1:
                        st.markdown("#### Sentiment Distribution")
                        st.info("Measures the overall polarity of customer feedback.")
                        sentiment_df = pd.DataFrame(list(sentiment_dist.items()), columns=['Sentiment', 'Count'])
                        color_discrete_map = {'Positive': '#00cc96', 'Negative': '#ef553b', 'Neutral': '#636efa'}
                        fig_sentiment = px.bar(sentiment_df, x='Sentiment', y='Count', color='Sentiment',
                                               color_discrete_map=color_discrete_map, text='Count')
                        fig_sentiment.update_traces(textposition='outside')
                        fig_sentiment.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                        st.plotly_chart(fig_sentiment, use_container_width=True)

                    with tab2:
                        st.markdown("#### Thematic Clusters (What are customers talking about?)")
                        st.info("Unsupervised extraction of key discussion themes.")
                        topic_df = pd.DataFrame(list(topic_dist.items()), columns=['Topic', 'Count'])
                        fig_topic = px.pie(topic_df, values='Count', names='Topic', hole=0.4,
                                           color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig_topic.update_traces(textposition='inside', textinfo='percent+label')
                        fig_topic.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                        st.plotly_chart(fig_topic, use_container_width=True)

                    with tab3:
                        st.markdown("#### Processed Review Data")
                        st.info("Export this table to dive deeper into specific issues.")
                        analysis_df = pd.DataFrame(result['analysis'])
                        st.dataframe(analysis_df, use_container_width=True, height=400)

                        csv = analysis_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="⬇️ Download Analyzed Data",
                            data=csv,
                            file_name='nlp_analysis_results.csv',
                            mime='text/csv',
                        )

                except Exception as e:
                    st.error(f"Error running NLP Analysis: {e}")

    except Exception as e:
        st.error(f"Error reading file: {e}")

else:
    # Landing Page State
    st.info("👈 Please upload a dataset from the sidebar to begin analysis.")
    st.markdown("""
    ### Why use this system?
    * **Stop Manual Reading:** Don't waste hours reading 1% of your reviews.
    * **Catch Issues Early:** Identify sudden spikes in specific complaints (e.g., 'Battery Drain').
    * **Objective Measurement:** Move beyond simple star ratings to understand *contextual* sentiment.
    """)
