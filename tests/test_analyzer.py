import pytest
import sys
sys.path.append('.')
from src.topic_analyzer import TopicAnalyzer, get_insights

def test_analyzer():
    analyzer = TopicAnalyzer()
    res = analyzer.analyze(["amazing battery", "broke terrible thing"])
    assert res[0]['sentiment'] == "Positive"
    assert res[0]['topic'] == "Battery Life"
    assert res[1]['sentiment'] == "Negative"

def test_get_insights():
    data = [{"topic": "A", "sentiment": "Pos"}, {"topic": "A", "sentiment": "Neg"}]
    insights = get_insights(data)
    assert insights['total_analyzed'] == 2
    assert insights['topic_distribution']['A'] == 2
