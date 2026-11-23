from curso_ia.retrieval import TfidfIndex

documents = [
    "Machine learning é um campo da inteligência artificial que permite que computadores aprendam padrões a partir de dados.",
    "O aprendizado de máquina dá aos sistemas a capacidade de melhorar seu desempenho sem serem explicitamente programados.",
    "Em vez de seguir apenas regras fixas, o machine learning descobre relações escondidas nos dados.",
    "Esse campo combina estatística, algoritmos e poder computacional para extrair conhecimento.",
    "O objetivo é criar modelos capazes de generalizar além dos exemplos vistos no treinamento.",
    "Aplicações de machine learning vão desde recomendações de filmes até diagnósticos médicos.",
    "Os algoritmos de aprendizado de máquina transformam dados brutos em previsões úteis.",
    "Diferente de um software tradicional, o ML adapta-se conforme novos dados chegam.",
    "O aprendizado pode ser supervisionado, não supervisionado ou por reforço, dependendo do tipo de problema.",
    "Na prática, machine learning é o motor que impulsiona muitos avanços em visão computacional e processamento de linguagem natural.",
    "Mais do que encontrar padrões, o machine learning ajuda a tomar decisões baseadas em evidências.",
]

index = TfidfIndex(documents)

print(f"documentos: {index.matrix.shape[0]}, vocabulário: {index.matrix.shape[1]} termos")

query = "machine learning"
print(f"\nconsulta: {query!r}")
print("vetor da consulta (termo -> peso):")
terms = index.vectorizer.get_feature_names_out()
row = index.query_vector(query)
for col, weight in zip(row.indices, row.data):
    print(f"  {terms[col]:<10} {weight:.3f}")

print("\nscore de cada documento:")
for i, score in enumerate(index.scores(query)):
    print(f"  doc {i:>2}: {score:.3f}")

print("\nranking (top 3):")
for i, score in index.search(query, top_k=3):
    print(f"  {score:.3f}  doc {i:>2}: {documents[i][:70]}...")
