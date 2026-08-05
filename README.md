# NLP Review Intelligence

A mock end-to-end NLP pipeline architecture for serving sentiment classification and topic modeling on product reviews.

## Problem / Motivation

This project explores an architectural setup for applying natural language processing (NLP) to customer reviews to extract sentiment and topic clusters. It focuses on the infrastructure to deploy text analysis pipelines via a FastAPI backend and an interactive Streamlit frontend.

## Approach

1. **Backend API:** A FastAPI application (`app/api.py`) exposing an `/analyze` endpoint to receive batch text payloads.
2. **Frontend Dashboard:** A Streamlit application (`app/streamlit_app.py`) for uploading CSV files containing reviews and visualizing sentiment distributions and topic clusters via Plotly.
3. **Analysis Logic:** A Python module (`src/`) containing a text preprocessor (using `spaCy` for tokenization and lemmatization) and a topic analyzer containing placeholder heuristic analysis logic.
4. **Notebooks:** Jupyter notebooks containing boilerplate code outlining workflows for exploratory data analysis, DistilBERT fine-tuning, and BERTopic modeling.

## Results

There are currently no trained models, quantitative metrics, or verifiable outputs in the repository. The application relies on rule-based placeholder logic.

## Tech Stack

- **Language:** Python 3.10
- **Data Processing & NLP:** pandas, numpy, spaCy, scikit-learn
- **Backend API:** FastAPI, uvicorn, pydantic, requests
- **Frontend & Visualization:** Streamlit, plotly, matplotlib, seaborn
- **Testing:** pytest
- **Deployment:** Render (via `render.yaml`)

## Project Structure

```text
.
├── app/
│   ├── api.py
│   └── streamlit_app.py
├── data/
│   └── amazon_reviews.csv
├── models/
│   └── .gitkeep
├── notebooks/
│   ├── 01_eda_text_analysis.ipynb
│   ├── 02_distilbert_finetune.ipynb
│   └── 03_bertopic_modeling.ipynb
├── src/
│   ├── __init__.py
│   ├── text_preprocessor.py
│   └── topic_analyzer.py
├── tests/
│   ├── test_analyzer.py
│   └── test_preprocessor.py
├── Dockerfile
├── render.yaml
├── requirements.txt
└── README.md
```

## How to Run Locally

1. Clone the repository and navigate to the root directory.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pytest spacy
   python -m spacy download en_core_web_sm
   ```
3. Run the backend API (in a separate terminal):
   ```bash
   uvicorn app.api:app --host 0.0.0.0 --port 8000
   ```
4. Run the Streamlit frontend:
   ```bash
   streamlit run app/streamlit_app.py
   ```
5. Run the test suite:
   ```bash
   pytest tests/
   ```

## Limitations & Future Work

- The sentiment analysis and topic modeling logic (`TopicAnalyzer`) is a hardcoded mock intended for testing the deployment infrastructure. It does not utilize actual DistilBERT or BERTopic machine learning models.
- The `models/` directory does not contain any trained model artifacts.
- The provided dataset (`data/amazon_reviews.csv`) contains 5 sample rows, acting as a structural mock rather than a training corpus.
- The Jupyter notebooks (`notebooks/`) contain unexecuted placeholder code and require full implementation for actual model training and evaluation.
- Future work would involve collecting a real dataset, implementing model training in the notebooks, serializing the trained model weights to the `models/` directory, and integrating those models into the FastAPI backend.

## Author / Links

Built by Mohammed Minhaj Mahmood
[LinkedIn](https://linkedin.com/in/muhammadminhaj229) · [GitHub](https://github.com/MuhammadMinhaj229)
