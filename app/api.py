from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import sys
sys.path.append('..')
from src.topic_analyzer import TopicAnalyzer, get_insights

app = FastAPI(title="NLP Review Intelligence API", version="1.0.0")

# Initialize models (mocked)
analyzer = TopicAnalyzer(model_path="../models")

class ReviewRequest(BaseModel):
    texts: List[str]

class InsightResponse(BaseModel):
    analysis: List[Dict[str, Any]]
    insights: Dict[str, Any]

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze", response_model=InsightResponse)
def analyze_reviews(request: ReviewRequest):
    if not request.texts:
        raise HTTPException(status_code=400, detail="No texts provided for analysis.")

    analysis_results = analyzer.analyze(request.texts)
    insights = get_insights(analysis_results)

    return {
        "analysis": analysis_results,
        "insights": insights
    }
