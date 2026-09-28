import re
import spacy


# Load spaCy English model
nlp = spacy.load("en_core_web_sm")


def clean_text(text):
    """
    Clean raw text.
    """

    if not text:
        return ""

    # Convert to lowercase
    text = text.lower()

    # Replace multiple spaces/newlines with one space
    text = re.sub(r"\s+", " ", text)

    # Remove unwanted characters
    text = re.sub(r"[^a-zA-Z0-9+#.\- ]", " ", text)

    # Remove extra spaces again
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def preprocess_text(text):
    """
    Perform basic NLP preprocessing using spaCy.
    """

    cleaned = clean_text(text)

    doc = nlp(cleaned)

    tokens = []

    for token in doc:

        if token.is_stop:
            continue

        if token.is_punct:
            continue

        if token.is_space:
            continue

        tokens.append(token.lemma_.lower())

    return " ".join(tokens)