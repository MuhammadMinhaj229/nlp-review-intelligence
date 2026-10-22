import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.topic_analyzer import TopicAnalyzer, get_insights

def test_analyzer():
    analyzer = TopicAnalyzer()
    res = analyzer.analyze(["amazing battery", "broke terrible thing"])
    assert res[0]['sentiment'] == "Positive"
    assert res[0]['topic'] == "Battery Life"
    assert res[1]['sentiment'] == "Negative"

def test_get_insights():
    data = [
        {"topic": "A", "aspect": "A", "sentiment": "Positive", "polarity": 0.5, "churn_risk_score": 10},
        {"topic": "A", "aspect": "A", "sentiment": "Negative", "polarity": -0.6, "churn_risk_score": 80}
    ]
    insights = get_insights(data)
    assert insights['total_analyzed'] == 2
    assert insights['topic_distribution']['A'] == 2
