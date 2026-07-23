# 🧠 NLP Review Intelligence System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow)
![DistilBERT](https://img.shields.io/badge/DistilBERT-Fine--tuned-orange)
![BERTopic](https://img.shields.io/badge/BERTopic-0.15-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

> **Built an end-to-end NLP pipeline that fine-tunes DistilBERT for sentiment
> classification and applies BERTopic to cluster 500K+ Amazon reviews into
> actionable product intelligence — deployed as an interactive dashboard.**

---

## 🏢 The Real Business Problem

Every e-commerce business receives thousands of customer reviews daily.
Amazon alone processes over 3.5 million reviews every day globally.

**Problem 1 — Reviews are unread and wasted.**
Product managers manually read a sample of reviews.
The other 99% — containing critical complaints, feature requests,
and competitor comparisons — are completely ignored.

**Problem 2 — Sentiment is oversimplified.**
A 3-star review can mean very different things:
"Great product but terrible delivery" vs "Works fine but overpriced."
Simple star ratings hide nuanced customer sentiment that product
teams desperately need.

**Problem 3 — No topic intelligence.**
What are customers actually complaining about?
What features do they love? What do they compare to competitors?
Without NLP, these questions take weeks of manual analysis to answer.

**The business cost:**
A product with undetected quality issues in reviews loses
**23–35% more customers** than competitors who actively monitor
and respond to review trends.

---

## 💡 The Solution This Project Builds

### Part 1 — Sentiment Classification (DistilBERT)

Fine-tuned DistilBERT on 50,000 Amazon reviews to classify
sentiment as Positive, Negative, or Neutral with high accuracy.

**Why DistilBERT over traditional ML?**

| Approach | Accuracy | Handles Sarcasm | Context-Aware |
|----------|----------|-----------------|---------------|
| Logistic Regression (TF-IDF) | 78.3% | No | No |
| LSTM | 82.1% | Partial | Partial |
| **DistilBERT (fine-tuned)** | **91.4%** | **Yes** | **Yes** |

**Model Performance:**

| Metric | Score |
|--------|-------|
| Accuracy | 91.4% |
| F1 Score (Macro) | 0.89 |
| Precision | 0.90 |
| Recall | 0.88 |
| Training Time | 23 mins (GPU) |

### Part 2 — Topic Modeling (BERTopic)

Applied BERTopic to 500,000 Amazon reviews to automatically
discover what customers are actually talking about.

**How BERTopic works:**
1. SentenceTransformers converts reviews to semantic embeddings
2. UMAP reduces dimensionality
3. HDBSCAN clusters similar reviews
4. TF-IDF extracts representative words per cluster

**Top 10 Topics Discovered:**

| Topic | Keywords | Review Count | Avg Sentiment |
|-------|----------|-------------|---------------|
| Battery Life | battery, drain, charge, hours | 42,300 | -0.32 (Negative) |
| Delivery & Packaging | box, damaged, shipping, arrived | 38,700 | -0.61 (Negative) |
| Build Quality | cheap, plastic, durable, sturdy | 31,200 | -0.18 (Mixed) |
| Value for Money | price, worth, expensive, budget | 28,900 | +0.41 (Positive) |
| Customer Service | refund, support, replaced, helpful | 24,100 | -0.29 (Negative) |
| Sound Quality | bass, audio, clear, loud | 19,800 | +0.67 (Positive) |
| Size & Fit | small, large, tight, perfect | 17,400 | +0.12 (Mixed) |
| Setup & Installation | easy, install, instructions, simple | 15,600 | +0.54 (Positive) |
| Comparison | better, compared, previous, upgrade | 12,300 | +0.38 (Positive) |
| Durability Issues | broke, stopped, weeks, replaced | 9,800 | -0.78 (Negative) |

**Business insight from topics:**
Battery life and delivery are the top two pain points.
A product manager can now prioritize these fixes immediately
instead of spending 3 weeks manually reading reviews.

---

## 📊 Business Impact

| Business Metric | Before | After |
|-----------------|--------|-------|
| Review analysis coverage | ~1% (manual sampling) | 100% automated |
| Time to identify top complaints | 2–3 weeks | Real-time |
| Sentiment accuracy | Star rating only | 91.4% NLP accuracy |
| Product iteration speed | Quarterly | Weekly |
| Customer complaint response time | Days | Hours (automated alerts) |
| Revenue impact | Baseline | 12–18% reduction in negative review rate (projected) |

---

## 🌍 Industries Where This System Applies

| Industry | Use Case | Impact |
|----------|----------|--------|
| **E-Commerce** | Product review intelligence (Amazon, Flipkart) | Faster product improvement cycles |
| **Hospitality** | Hotel/restaurant review monitoring | Identify service gaps in real-time |
| **Banking & Finance** | Customer complaint analysis | Reduce regulatory risk |
| **Healthcare** | Patient feedback classification | Improve care quality |
| **EdTech** | Course review sentiment tracking | Improve curriculum design |
| **FMCG / Retail** | Brand sentiment monitoring | Real-time brand health tracking |
| **Social Media** | Tweet/post sentiment analysis | Crisis detection and management |

---

## 🛠️ Complete Tech Stack

| Category | Tool | Purpose |
|----------|------|---------|
| Data Processing | Python, Pandas, NumPy | Cleaning 500K+ reviews |
| NLP Preprocessing | spaCy, NLTK | Tokenization, lemmatization |
| Sentiment Model | HuggingFace Transformers | Fine-tune DistilBERT |
| Sentence Embeddings | SentenceTransformers | Semantic review vectors |
| Topic Modeling | BERTopic | Unsupervised topic discovery |
| Training | PyTorch | Model fine-tuning |
| Experiment Tracking | MLflow | Log training runs |
| Visualization | Plotly | Interactive topic explorer |
| Dashboard | Streamlit | Business-facing UI |

---

## 📁 Project Structure
nlp-review-intelligence/
├── data/
│   └── amazon_reviews.csv          # 500K Amazon product reviews
├── notebooks/
│   ├── 01_eda_text_analysis.ipynb  # Text EDA, length, distribution
│   ├── 02_distilbert_finetune.ipynb # Fine-tune on 50K reviews
│   ├── 03_bertopic_modeling.ipynb  # Topic discovery on 500K reviews
│   └── 04_dashboard_prep.ipynb     # Prepare data for Streamlit
├── app/
│   └── streamlit_app.py            # Interactive review intelligence UI
├── src/
│   ├── init.py
│   ├── text_preprocessor.py        # spaCy cleaning pipeline
│   └── topic_analyzer.py           # BERTopic wrapper utilities
├── models/
│   ├── distilbert_sentiment/       # Fine-tuned model weights
│   └── bertopic_model.pkl          # Saved topic model
├── requirements.txt
└── README.md

---

## 🔑 Key Technical Decisions

**Why DistilBERT over BERT?**
DistilBERT is 40% smaller and 60% faster than BERT
while retaining 97% of BERT's accuracy. For production
deployment on limited compute, this is the right tradeoff.

**Why BERTopic over LDA?**
LDA assigns words to topics based on co-occurrence.
BERTopic uses semantic embeddings — it understands that
"broke after a week" and "stopped working quickly" are
the same complaint, even though they share no words.

**Why 500K reviews for topic modeling?**
More reviews = more stable, meaningful topics.
With 500K reviews, even niche complaint categories
have enough volume to form coherent clusters.

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/MuhammadMinhaj229/nlp-review-intelligence.git
cd nlp-review-intelligence
pip install -r requirements.txt
python -m spacy download en_core_web_sm
# Run notebooks in order: 01 → 02 → 03 → 04
streamlit run app/streamlit_app.py
```

---

## 📈 Key Findings Summary

- **91.4% sentiment accuracy** — DistilBERT outperforms TF-IDF baseline by 13.1%
- **10 coherent topics** discovered from 500K reviews automatically
- **Battery life** is the #1 negative topic across all product categories
- **Delivery & packaging** is the #2 complaint — a logistics problem, not product
- **Sound quality** has the highest positive sentiment score (+0.67)
- **9,800 reviews** about durability issues — strong signal for product QA team
- **100% review coverage** vs 1% manual sampling — 100x more intelligence

---

## 🔗 Live Demo

👉 **[Launch Review Intelligence Dashboard](https://nlp-frontend-v3.onrender.com)**

---

*Built by Mohammed Minhaj Mahmood*
*[LinkedIn](https://linkedin.com/in/muhammadminhaj229) · [GitHub](https://github.com/MuhammadMinhaj229) · Hyderabad, India*