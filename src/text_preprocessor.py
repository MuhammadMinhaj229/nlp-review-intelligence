import re
from typing import List

STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
    "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't",
    "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't",
    "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm",
    "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more",
    "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
    "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that",
    "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these",
    "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too",
    "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who",
    "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll",
    "you're", "you've", "your", "yours", "yourself", "yourselves"
}

def clean_text(text: str) -> str:
    """Removes HTML, non-alphabetic characters, and normalizes whitespace."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def stem_or_lemmatize(word: str) -> str:
    """Lightweight deterministic morphological normalizer."""
    if word.endswith("ing") and len(word) > 4:
        base = word[:-3]
        if len(base) >= 3 and base[-1] == base[-2] and base[-1] not in "lsz":
            base = base[:-1]
        return base
    if word.endswith("ed") and len(word) > 4:
        base = word[:-2]
        if len(base) >= 3 and base[-1] == base[-2] and base[-1] not in "lsz":
            base = base[:-1]
        return base
    if word.endswith("s") and not word.endswith("ss") and len(word) > 3:
        return word[:-1]
    return word

def preprocess_text(text: str) -> str:
    """Cleans, tokenizes, removes stopwords, and normalizes tokens."""
    cleaned = clean_text(text)
    if not cleaned:
        return ""
    tokens = cleaned.split()
    normalized = []
    for t in tokens:
        if t not in STOPWORDS and len(t) > 1:
            norm = stem_or_lemmatize(t)
            normalized.append(norm)
    return " ".join(normalized)

def preprocess_batch(texts: List[str]) -> List[str]:
    """Processes a batch of raw strings."""
    return [preprocess_text(t) for t in texts]
