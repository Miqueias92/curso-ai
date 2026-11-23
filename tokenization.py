import nltk

"""
O NLTK (Natural Language Toolkit) possui alguns recursos relacionados à divisão de palavras, mas não oferece implementação nativa dos principais algoritmos modernos de Subword Tokenization, como BPE, WordPiece e Unigram.
O foco principal do NLTK é o processamento tradicional de linguagem natural.
"""


nltk.download("punkt_tab")

text = "Machine learning é um campo da inteligência artificial que permite que computadores aprendam padrões a partir de dados. Sem serem programados explicitamente para cada tarefa."

word_tokens = nltk.word_tokenize(text)
print(word_tokens)

print("\n\n\n")

sentence_tokens = nltk.sent_tokenize(text)

print("senteces tokens")
print(sentence_tokens)


# pre processamento sem alfa numérico,
def preprossing(text):
    # transforma para lower
    tokens = nltk.word_tokenize(text.lower())

    # remove palavras não alfnumerios
    return [word for word in tokens if word]


# pre proessamento com alfa numérico para mostrar a diferença do texto final
def preprossing_alfa(text):
    # transforma para lower
    tokens = nltk.word_tokenize(text.lower())

    # remove palavras não alfnumerios
    return [word for word in tokens if word.isalnum()]


documents = [
    "Machine learning é o aprendizado automático de máquinas a partir de dados.",
    "Ele permite que sistemas façam previsões e decisões sem programação explícita.",
    "É usado em áreas como reconhecimento de voz, imagens e recomendação de conteúdo.",
]

print("\n\n\n\npre processa os tokens sem eliminar alfa numérico")

# aqui " ".join é apenas a título de exemplo, para a leitura do print ficar mais simples
# mas na prática " ".join() estaria "revertendo" o word_tokenize, e não faria sentido usar
preprocessed_docs = [" ".join(preprossing(doc)) for doc in documents]
print(preprocessed_docs)

print("\n\n\n\npre processa os tokens com alfa numérico e sem join")
preprocessed_docs = [preprossing_alfa(doc) for doc in documents]
print(preprocessed_docs)
