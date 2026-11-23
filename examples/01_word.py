from curso_ia.tokenization import preprocess, word_tokenize

text = "Machine learning é um campo da inteligência artificial que permite que computadores aprendam padrões a partir de dados."

print("word_tokenize:")
print(word_tokenize(text))

print("\npré-processado (minúsculas, sem pontuação):")
print(preprocess(text))

print("\npré-processado (minúsculas, mantendo pontuação):")
print(preprocess(text, only_alnum=False))
