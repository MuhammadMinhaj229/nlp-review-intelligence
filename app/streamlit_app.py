import streamlit as st
import pandas as pd
import requests
import json
import plotly.express as px

# Configuration
API_URL = "http://localhost:8000"

st.set_page_config(page_title="Review Intelligence", page_icon="🧠", layout="wide")

st.title("🧠 NLP Review Intelligence Dashboard")
st.markdown("Analyze customer reviews for sentiment and latent topics.")

# File upload
uploaded_file = st.file_uploader("Upload CSV of Reviews", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(f"Loaded {len(df)} reviews.")

    if st.button("Analyze Reviews"):
        with st.spinner("Analyzing..."):
            texts = df['review_text'].dropna().tolist()

            try:
                response = requests.post(f"{API_URL}/analyze", json={"texts": texts})
                response.raise_for_status()
                result = response.json()

                # Display Insights
                st.subheader("Analysis Insights")
                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Topic Distribution**")
                    topic_dist = result['insights']['topic_distribution']
                    topic_df = pd.DataFrame(list(topic_dist.items()), columns=['Topic', 'Count'])
                    fig_topic = px.pie(topic_df, values='Count', names='Topic', title='Topics')
                    st.plotly_chart(fig_topic, use_container_width=True)

                with col2:
                    st.write("**Sentiment Distribution**")
                    sentiment_dist = result['insights']['sentiment_distribution']
                    sentiment_df = pd.DataFrame(list(sentiment_dist.items()), columns=['Sentiment', 'Count'])
                    fig_sentiment = px.bar(sentiment_df, x='Sentiment', y='Count', title='Sentiments', color='Sentiment')
                    st.plotly_chart(fig_sentiment, use_container_width=True)

                st.subheader("Raw Results")
                st.dataframe(pd.DataFrame(result['analysis']))

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to API: {e}")
                st.info("Make sure the FastAPI backend is running.")

else:
    st.info("Upload a CSV file with a 'review_text' column to get started.")
