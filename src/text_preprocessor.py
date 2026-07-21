import re
import spacy
from typing import List, Union

# Load spaCy model, suppress output
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def clean_text(text: str) -> str:
    """Removes HTML, special characters, and extra whitespace."""
    if not isinstance(text, str):
        return ""

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Remove non-alphabetic characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase and strip whitespace
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)

    return text

def preprocess_text(text: str) -> str:
    """Cleans, tokenizes, removes stopwords, and lemmatizes text using spaCy."""
    cleaned = clean_text(text)
    if not cleaned:
        return ""

    doc = nlp(cleaned)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and len(token.lemma_) > 1]

    return " ".join(tokens)

def preprocess_batch(texts: List[str]) -> List[str]:
    """Process a batch of texts for efficiency."""
    # Using nlp.pipe for efficient batch processing
    cleaned_texts = [clean_text(t) for t in texts]
    docs = nlp.pipe(cleaned_texts, batch_size=50)

    results = []
    for doc in docs:
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and len(token.lemma_) > 1]
        results.append(" ".join(tokens))

    return results
