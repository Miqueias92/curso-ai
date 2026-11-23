from curso_ia.tokenization import sentence_tokenize

text = (
    "Machine learning é um campo da inteligência artificial. "
    "O Dr. Silva estuda o tema desde 2010. "
    "Sem serem programados explicitamente, os computadores aprendem com dados."
)

for i, sentence in enumerate(sentence_tokenize(text), start=1):
    print(f"{i}: {sentence}")
