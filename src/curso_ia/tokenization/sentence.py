"""Tokenização por sentença (NLTK)."""

import nltk

from curso_ia.tokenization._nltk import ensure_punkt


def sentence_tokenize(text: str, language: str = "portuguese") -> list[str]:
    """Divide o texto em sentenças."""
    ensure_punkt()
    return nltk.sent_tokenize(text, language=language)
