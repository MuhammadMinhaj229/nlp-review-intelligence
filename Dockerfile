FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install setuptools wheel && pip install --no-cache-dir -r requirements.txt
RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0.tar.gz

COPY . .

# Expose API and Streamlit ports
EXPOSE 8000
EXPOSE 8501

# Command to run both (for simplicity in a single container demo)
CMD ["sh", "-c", "uvicorn app.api:app --host 0.0.0.0 --port 8000 & streamlit run app/streamlit_app.py --server.port 8501 --server.address 0.0.0.0"]
