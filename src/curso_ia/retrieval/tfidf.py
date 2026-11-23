"""Busca por TF-IDF e similaridade do cosseno (scikit-learn)."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from curso_ia.tokenization import preprocess


def _normalize(text: str) -> str:
    """Minúsculas, sem pontuação, tokens separados por espaço."""
    return " ".join(preprocess(text))


class TfidfIndex:
    """Índice TF-IDF sobre uma lista de documentos."""

    def __init__(self, documents: list[str]) -> None:
        self.documents = documents
        self.vectorizer = TfidfVectorizer()
        self.matrix = self.vectorizer.fit_transform(_normalize(d) for d in documents)

    def query_vector(self, query: str):
        """Vetor TF-IDF da consulta, no mesmo espaço dos documentos."""
        return self.vectorizer.transform([_normalize(query)])

    def scores(self, query: str) -> list[float]:
        """Cosseno entre a consulta e cada documento, na ordem original."""
        return cosine_similarity(self.matrix, self.query_vector(query)).flatten().tolist()

    def search(self, query: str, top_k: int = 3) -> list[tuple[int, float]]:
        """Retorna (índice do documento, score) dos top_k mais relevantes."""
        ranked = sorted(enumerate(self.scores(query)), key=lambda p: p[1], reverse=True)
        return ranked[:top_k]
