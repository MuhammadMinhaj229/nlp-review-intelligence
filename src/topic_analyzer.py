import re
from typing import List, Dict, Any
import pandas as pd
from collections import Counter

POSITIVE_WORDS = {
    "amazing", "exceptional", "superb", "outstanding", "great", "excellent", "flawless",
    "good", "solid", "crisp", "intuitive", "seamless", "fast", "pristine", "quietly",
    "essential", "love", "perfect", "easy", "satisfied", "helpful", "reliable", "best"
}

NEGATIVE_WORDS = {
    "terrible", "broke", "crushed", "missing", "expensive", "lacking", "crashes", "crash",
    "damaged", "poor", "muffled", "refused", "uncomfortably", "hot", "rain", "fragile",
    "frustrating", "charged twice", "complained", "delayed", "horrible", "awful", "bad", "worst"
}

ASPECT_PATTERNS = {
    "Battery Life": ["battery", "charge", "charging", "standby", "battery life"],
    "Product Quality": ["build quality", "construction", "hardware", "screen", "glare", "thermal", "heating", "acoustics", "bass", "sound", "microphone", "plastic", "durability"],
    "Logistics & Delivery": ["delivery", "shipping", "package", "packaging", "carrier", "parcel", "box", "transit", "delay", "curb", "tracking"],
    "Pricing & Billing": ["price", "pricing", "expensive", "cost", "billing", "charged", "subscription", "seat renewal", "renewal", "discounted"],
    "Customer Support": ["customer support", "customer service", "support", "warranty", "turnaround", "agent", "chat", "resolution", "refund"],
    "Software & Usability": ["interface", "ui", "ux", "crash", "crashes", "bluetooth", "pairing", "api", "synchronization", "sync", "export", "firmware", "productivity"]
}

CHURN_INTENT_PATTERNS = [
    r"do not buy", r"never buy", r"switching to", r"canceling", r"cancelled", r"refused",
    r"charged twice", r"broke after", r"terrible", r"worst", r"unacceptable", r"waste of money"
]

class TopicAnalyzer:
    """Enterprise Review Intelligence and Voice-of-Customer (VoC) Analyzer."""

    def __init__(self, model_path: str = None):
        self.model_path = model_path

    def analyze_single(self, text: str, review_id: Any = None) -> Dict[str, Any]:
        """Analyzes a single review for sentiment, aspect classification, and churn risk."""
        lower_text = text.lower() if isinstance(text, str) else ""

        # Identify Primary Aspect / Topic
        assigned_aspect = "General"
        # Check specific Battery Life priority for backward compatibility
        if any(term in lower_text for term in ASPECT_PATTERNS["Battery Life"]):
            assigned_aspect = "Battery Life"
        else:
            for aspect, keywords in ASPECT_PATTERNS.items():
                if any(k in lower_text for k in keywords):
                    assigned_aspect = aspect
                    break

        # Calculate Polarity and Sentiment
        pos_hits = sum(1 for w in POSITIVE_WORDS if w in lower_text)
        neg_hits = sum(1 for w in NEGATIVE_WORDS if w in lower_text)

        if pos_hits > neg_hits:
            sentiment = "Positive"
            polarity = min(1.0, 0.4 + (pos_hits * 0.2))
        elif neg_hits > pos_hits:
            sentiment = "Negative"
            polarity = max(-1.0, -0.4 - (neg_hits * 0.2))
        else:
            sentiment = "Neutral"
            polarity = 0.0

        confidence = round(min(0.98, 0.65 + (abs(polarity) * 0.3)), 2)

        # Churn Risk & Escalation Scoring (0 to 100)
        churn_score = 15
        if sentiment == "Negative":
            churn_score += 40
            churn_score += min(30, neg_hits * 15)
        elif sentiment == "Neutral":
            churn_score += 10
        else:
            churn_score = max(5, 20 - (pos_hits * 5))

        has_churn_intent = any(re.search(pat, lower_text) for pat in CHURN_INTENT_PATTERNS)
        if has_churn_intent:
            churn_score = min(100, churn_score + 25)

        churn_score = min(100, max(0, churn_score))

        if churn_score >= 70:
            risk_level = "Critical"
            escalation = "Immediate Action Required"
        elif churn_score >= 45:
            risk_level = "High"
            escalation = "Review Needed"
        elif churn_score >= 25:
            risk_level = "Medium"
            escalation = "Monitor"
        else:
            risk_level = "Low"
            escalation = "Satisfied"

        return {
            "review_id": review_id,
            "text": text,
            "topic": assigned_aspect,
            "aspect": assigned_aspect,
            "sentiment": sentiment,
            "polarity": round(polarity, 2),
            "confidence": confidence,
            "churn_risk_score": churn_score,
            "churn_risk_level": risk_level,
            "escalation_priority": escalation
        }

    def analyze(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Processes a list of review texts."""
        return [self.analyze_single(text, review_id=idx + 1) for idx, text in enumerate(texts)]

def get_insights(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generates executive Voice-of-Customer KPIs and diagnostic aggregations."""
    if not data:
        return {}

    df = pd.DataFrame(data)
    total_analyzed = len(df)

    topic_counts = df['topic'].value_counts().to_dict()
    sentiment_dist = df['sentiment'].value_counts().to_dict()

    pos_count = sentiment_dist.get('Positive', 0)
    neg_count = sentiment_dist.get('Negative', 0)
    neu_count = sentiment_dist.get('Neutral', 0)

    # Net Sentiment Score: (% Positive - % Negative), ranges from -100 to +100
    net_sentiment_score = round(((pos_count - neg_count) / total_analyzed) * 100, 1) if total_analyzed > 0 else 0.0

    # Churn Risk Distribution
    risk_counts = df['churn_risk_level'].value_counts().to_dict() if 'churn_risk_level' in df.columns else {}
    critical_count = risk_counts.get('Critical', 0) + risk_counts.get('High', 0)
    churn_risk_pct = round((critical_count / total_analyzed) * 100, 1) if total_analyzed > 0 else 0.0

    # Average polarity per aspect
    aspect_breakdown = {}
    if 'aspect' in df.columns and 'polarity' in df.columns:
        for aspect, group in df.groupby('aspect'):
            aspect_breakdown[aspect] = {
                "count": int(len(group)),
                "avg_polarity": round(float(group['polarity'].mean()), 2),
                "negative_count": int(sum(group['sentiment'] == 'Negative')),
                "positive_count": int(sum(group['sentiment'] == 'Positive'))
            }

    # Extract Key Drivers
    all_words = []
    if 'text' in df.columns:
        for text in df['text'].dropna():
            words = re.findall(r'[a-zA-Z]{4,}', text.lower())
            all_words.extend([w for w in words if w in POSITIVE_WORDS or w in NEGATIVE_WORDS])
    driver_counts = Counter(all_words).most_common(6)

    # Priority escalation queue for immediate resolution
    escalation_queue = []
    if 'churn_risk_score' in df.columns:
        critical_df = df[df['churn_risk_score'] >= 50].sort_values(by='churn_risk_score', ascending=False)
        for _, row in critical_df.head(10).iterrows():
            escalation_queue.append({
                "review_id": row.get('review_id', 'N/A'),
                "aspect": row.get('aspect', 'General'),
                "sentiment": row.get('sentiment', 'Negative'),
                "churn_risk_score": row.get('churn_risk_score', 0),
                "text": row.get('text', '')[:140] + ('...' if len(row.get('text', '')) > 140 else '')
            })

    return {
        "total_analyzed": total_analyzed,
        "sentiment_distribution": sentiment_dist,
        "topic_distribution": topic_counts,
        "aspect_breakdown": aspect_breakdown,
        "net_sentiment_score": net_sentiment_score,
        "churn_risk_percentage": churn_risk_pct,
        "churn_risk_distribution": risk_counts,
        "key_drivers": driver_counts,
        "escalation_queue": escalation_queue
    }
