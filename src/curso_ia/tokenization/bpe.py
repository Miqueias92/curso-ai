"""BPE (Byte Pair Encoding) didático, implementado do zero.

Algoritmo:
1. Cada palavra vira uma sequência de caracteres + marcador de fim "</w>".
2. Conta todos os pares de símbolos adjacentes no corpus.
3. Junta o par mais frequente em um novo símbolo (uma "merge").
4. Repete o passo 2-3 `num_merges` vezes. A lista de merges é o "modelo".
"""

from collections import Counter

END = "</w>"
Pair = tuple[str, str]
Vocab = dict[tuple[str, ...], int]


def _build_vocab(corpus: list[str]) -> Vocab:
    """Conta as palavras e as quebra em caracteres."""
    counts = Counter(word for line in corpus for word in line.lower().split())
    return {tuple(word) + (END,): freq for word, freq in counts.items()}


def _pair_counts(vocab: Vocab) -> Counter:
    pairs: Counter = Counter()
    for symbols, freq in vocab.items():
        for pair in zip(symbols, symbols[1:]):
            pairs[pair] += freq
    return pairs


def _merge(symbols: tuple[str, ...], pair: Pair) -> tuple[str, ...]:
    merged: list[str] = []
    i = 0
    while i < len(symbols):
        if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == pair:
            merged.append(symbols[i] + symbols[i + 1])
            i += 2
        else:
            merged.append(symbols[i])
            i += 1
    return tuple(merged)


def train_bpe(corpus: list[str], num_merges: int) -> list[Pair]:
    """Aprende a lista ordenada de merges a partir do corpus."""
    vocab = _build_vocab(corpus)
    merges: list[Pair] = []
    for _ in range(num_merges):
        pairs = _pair_counts(vocab)
        if not pairs:
            break
        best = max(pairs, key=lambda p: (pairs[p], p))  # desempate determinístico
        merges.append(best)
        vocab = {_merge(s, best): f for s, f in vocab.items()}
    return merges


def bpe_encode(word: str, merges: list[Pair]) -> list[str]:
    """Tokeniza uma palavra aplicando as merges na ordem em que foram aprendidas."""
    symbols = tuple(word.lower()) + (END,)
    for pair in merges:
        symbols = _merge(symbols, pair)
    return list(symbols)


def bpe_tokenize(text: str, merges: list[Pair]) -> list[str]:
    """Tokeniza um texto inteiro (separando por espaço)."""
    return [tok for word in text.split() for tok in bpe_encode(word, merges)]
