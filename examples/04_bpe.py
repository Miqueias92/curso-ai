from curso_ia.tokenization import bpe_encode, train_bpe

corpus = [
    "low low low low low",
    "lower lower",
    "newest newest newest newest newest newest",
    "widest widest widest",
]

merges = train_bpe(corpus, num_merges=10)

print("merges aprendidas (em ordem):")
for i, pair in enumerate(merges, start=1):
    print(f"{i:>2}. {pair[0]} + {pair[1]} -> {pair[0] + pair[1]}")

print("\ntokenizando palavras:")
for word in ["lowest", "newer", "wider", "low"]:
    print(f"{word:>8} -> {bpe_encode(word, merges)}")
