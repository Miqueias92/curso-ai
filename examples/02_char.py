from curso_ia.tokenization import char_tokenize

text = "Olá, IA!"
tokens = char_tokenize(text)

print(tokens)
print(f"{len(text)} caracteres -> {len(tokens)} tokens")
print("vocabulário:", sorted(set(tokens)))
