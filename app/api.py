from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.topic_analyzer import TopicAnalyzer, get_insights

app = FastAPI(
    title="Customer Voice Intelligence API",
    description="Enterprise NLP service for Aspect-Based Sentiment Analysis (ABSA) and customer churn risk quantification.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = TopicAnalyzer()

class ReviewItem(BaseModel):
    review_id: Optional[Any] = None
    text: str = Field(..., min_length=1, description="Raw feedback or review string.")

class SingleAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1)
    review_id: Optional[Any] = None

class BatchAnalysisRequest(BaseModel):
    texts: Optional[List[str]] = None
    reviews: Optional[List[ReviewItem]] = None

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "customer-voice-intelligence",
        "engine_version": "2.0.0"
    }

@app.post("/api/v1/analyze-single")
def analyze_single_review(req: SingleAnalysisRequest):
    return analyzer.analyze_single(req.text, req.review_id)

@app.post("/api/v1/analyze-batch")
@app.post("/analyze")
def analyze_reviews(request: BatchAnalysisRequest):
    raw_texts = []
    if request.reviews:
        raw_texts = [r.text for r in request.reviews]
    elif request.texts:
        raw_texts = request.texts
    else:
        raise HTTPException(status_code=400, detail="Provide 'texts' or 'reviews' in request payload.")

    analysis_results = analyzer.analyze(raw_texts)
    insights = get_insights(analysis_results)

    return {
        "analysis": analysis_results,
        "insights": insights
    }
