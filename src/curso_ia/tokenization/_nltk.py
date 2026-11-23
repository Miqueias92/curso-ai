"""Garante que os recursos do NLTK estejam baixados."""

import nltk


def ensure_punkt() -> None:
    try:
        nltk.data.find("tokenizers/punkt_tab")
    except LookupError:
        nltk.download("punkt_tab", quiet=True)
