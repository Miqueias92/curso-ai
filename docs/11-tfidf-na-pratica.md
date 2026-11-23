# 11. TF-IDF na prática (scikit-learn)

O [capítulo 09](09-vector-space-model.md) mostra a teoria e uma conta à mão. Aqui o mesmo modelo roda sobre 11 frases sobre machine learning, usando `TfidfVectorizer` e `cosine_similarity` do scikit-learn.

Código da aula original: [`src/aula/tokenization_tf_idf.py`](../src/aula/tokenization_tf_idf.py).
Versão estruturada: [`src/curso_ia/retrieval/tfidf.py`](../src/curso_ia/retrieval/tfidf.py) e [`examples/05_tfidf.py`](../examples/05_tfidf.py).

## O pipeline

```
documentos -> pré-processamento -> TfidfVectorizer.fit_transform -> matriz TF-IDF
consulta   -> pré-processamento -> vectorizer.transform           -> vetor da consulta
                                   cosine_similarity(matriz, vetor) -> score por documento
```

### 1. Pré-processamento

Reaproveita o `preprocess` da [tokenização por palavra](02-tokenizacao-por-palavra.md): minúsculas, `nltk.word_tokenize` e descarte do que não é alfanumérico. Depois os tokens são unidos por espaço, porque o `TfidfVectorizer` recebe texto e faz a própria separação.

```python
def _normalize(text):
    return " ".join(preprocess(text))
```

Pré-processar a consulta do mesmo jeito que os documentos é obrigatório. Se um lado ficasse em maiúsculas ou com pontuação, os termos não casariam.

### 2. Matriz TF-IDF

```python
vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(docs_normalizados)
```

- `fit` aprende o vocabulário e o IDF de cada termo a partir da coleção.
- `transform` converte cada documento em um vetor com uma dimensão por termo.
- O resultado é uma matriz **esparsa** (`scipy.sparse`): guarda só as posições diferentes de zero. Por isso `print(tfidf_matrix)` mostra linhas do tipo `(documento, termo) peso`, e não uma tabela cheia de zeros.
- Aqui são 11 documentos e 106 termos.

### 3. Vetor da consulta

```python
query_vector = vectorizer.transform(["machine learning"])
```

Usa `transform`, não `fit_transform`. A consulta precisa ser projetada no vocabulário e nos IDFs **da coleção**. Termos que não existem na coleção são ignorados.

Saída real:

```
  learning   0.707
  machine    0.707
```

Os dois pesos são iguais (0,707 = 1/√2) porque o scikit-learn normaliza cada vetor para norma 1 (`norm="l2"`) e os dois termos têm o mesmo TF e o mesmo IDF.

### 4. Cosseno

```python
cosine_similarity(matrix, query_vector).flatten()
```

Como todos os vetores já têm norma 1, o cosseno equivale ao produto escalar. O `flatten` transforma a matriz (11×1) em uma lista de 11 scores.

## Resultado

```
ranking (top 3):
  0.279  doc  5: Aplicações de machine learning vão desde recomendações de filmes...
  0.268  doc 10: Mais do que encontrar padrões, o machine learning ajuda a tomar...
  0.261  doc  2: Em vez de seguir apenas regras fixas, o machine learning descobre...
```

Rodar: `uv run python examples/05_tfidf.py`

## O que observar

- **Os scores são parecidos (0,24 a 0,28).** Todos os documentos que contêm os dois termos aparecem uma vez cada. A diferença vem do tamanho do documento: a norma divide o peso, então frases mais curtas pontuam um pouco mais.
- **Documentos sem os termos recebem 0.** O doc 1 ("O aprendizado de máquina dá aos sistemas...") fala do mesmo assunto, mas não contém "machine" nem "learning". O doc 7 usa "ML". É a limitação de **casamento léxico** do [capítulo 09](09-vector-space-model.md): sinônimos e traduções são dimensões sem relação. Resolver isso é o papel dos embeddings.
- **O ranking é de relevância, não um filtro.** Ao contrário do [boolean retrieval](08-boolean-retrieval.md), todos os documentos recebem uma nota e a ordem é o resultado.

## Limitações desta versão

- A tokenização é só por palavra: sem stemming, lematização nem remoção de stopwords. "aprendizado" e "aprendam" são termos diferentes.
- O índice é uma matriz em memória, sem índice invertido. Serve para estudo, não para milhões de documentos.
- `TfidfVectorizer` usa uma variação do IDF com suavização (`log((1+N)/(1+df)) + 1`), então os números diferem um pouco da conta à mão do capítulo 09.

## Referências

- [scikit-learn: TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- [scikit-learn: cosine_similarity](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html)
- [scikit-learn: Text feature extraction](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)
