"""Tokenização por palavra (NLTK)."""

import nltk

from curso_ia.tokenization._nltk import ensure_punkt


def word_tokenize(text: str) -> list[str]:
    """Divide o texto em palavras e pontuações."""
    ensure_punkt()
    return nltk.word_tokenize(text)


def preprocess(text: str, only_alnum: bool = True) -> list[str]:
    """Põe em minúsculas e, opcionalmente, mantém só tokens alfanuméricos."""
    tokens = word_tokenize(text.lower())
    if only_alnum:
        return [t for t in tokens if t.isalnum()]
    return tokens
