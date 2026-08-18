from pathlib import Path
import re

KNOWLEDGE_BASE_PATH = Path("data/knowledge_base")


def load_knowledge_base():
    """
    Load all text files from the knowledge base folder.
    """
    documents = []
    for file in KNOWLEDGE_BASE_PATH.glob("*.txt"):

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        documents.append({
            "filename": file.name,
            "content": content
        })

    return documents

def preprocess_text(text):
    """
    Convert text to lowercase and remove punctuation.
    Returns a list of words.
    """

    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)

    return text.split()

def search_knowledge_base(query):
    """
    Search the knowledge base using keyword matching.
    Returns the most relevant document.
    """

    documents = load_knowledge_base()

    query_words = preprocess_text(query)

    best_document = None
    highest_score = -1

    for document in documents:

        document_words = preprocess_text(document["content"])

        score = 0

        for word in query_words:
            if word in document_words:
                score += 1

        if score > highest_score:
            highest_score = score
            best_document = document

    return best_document