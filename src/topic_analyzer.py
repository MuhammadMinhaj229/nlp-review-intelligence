import pandas as pd
from typing import List, Dict, Any

class TopicAnalyzer:
    """Wrapper for analyzing topics and sentiments."""

    def __init__(self, model_path: str = None):
        # In a real scenario, this would load the BERTopic and DistilBERT models.
        self.model_path = model_path
        print(f"Initialized TopicAnalyzer with model from {self.model_path}")

    def analyze(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Mock analysis returning dummy topics and sentiments."""
        results = []
        for text in texts:
            # Dummy logic for demonstration
            topic = "Battery Life" if "battery" in text.lower() else "General"
            sentiment = "Positive" if "amazing" in text.lower() else "Negative" if "terrible" in text.lower() or "broke" in text.lower() else "Neutral"
            results.append({
                "text": text,
                "topic": topic,
                "sentiment": sentiment
            })
        return results

def get_insights(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate insights from analysis results."""
    df = pd.DataFrame(data)
    if df.empty:
        return {}

    topic_counts = df['topic'].value_counts().to_dict()
    sentiment_dist = df['sentiment'].value_counts().to_dict()

    return {
        "topic_distribution": topic_counts,
        "sentiment_distribution": sentiment_dist,
        "total_analyzed": len(df)
    }
