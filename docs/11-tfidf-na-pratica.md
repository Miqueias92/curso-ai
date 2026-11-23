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

## Entendendo `fit`, `transform` e a matriz

Esta seção responde três dúvidas comuns: o que o `fit_transform` faz, por que a consulta usa só `transform` e por que tudo vira uma matriz. Para ver os números inteiros, usamos 3 documentos pequenos:

```python
docs = ["gato come peixe", "gato dorme", "cachorro come osso"]
vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(docs)
```

### O que o `fit_transform` faz

São duas etapas em uma chamada.

**`fit`: aprender com a coleção.** O vectorizer lê todos os documentos e guarda duas coisas:

1. **O vocabulário.** Os termos distintos, em ordem alfabética, cada um com um número de coluna.

```python
vectorizer.get_feature_names_out()
# ['cachorro', 'come', 'dorme', 'gato', 'osso', 'peixe']
#      0         1       2       3       4       5
```

2. **O IDF de cada termo.** Quanto mais documentos contêm o termo, menor o IDF.

```python
vectorizer.idf_
# cachorro 1.69 | come 1.29 | dorme 1.69 | gato 1.29 | osso 1.69 | peixe 1.69
```

"gato" e "come" aparecem em 2 dos 3 documentos e valem menos (1,29). Os outros aparecem em 1 só e valem mais (1,69).

**`transform`: converter texto em vetor.** Com o vocabulário e os IDFs guardados, cada documento vira uma lista de 6 números, um por termo. Cada número é `TF × IDF`, e depois o vetor é normalizado para ter norma 1.

```python
matrix.toarray().round(2)
```

```
             cachorro  come  dorme  gato  osso  peixe
doc 0 (gato come peixe)   0.00  0.52  0.00  0.52  0.00  0.68
doc 1 (gato dorme)        0.00  0.00  0.80  0.61  0.00  0.00
doc 2 (cachorro come osso) 0.62 0.47  0.00  0.00  0.62  0.00
```

Leitura: o doc 0 tem peso em `come`, `gato` e `peixe`. `peixe` pesa mais (0,68) porque é raro. Onde o termo não aparece, o valor é 0.

### Por que a consulta usa só `transform`

Analogia: o `fit` monta uma **régua** com a coleção (quais termos existem e o quanto cada um é raro). O `transform` mede qualquer texto com essa régua. A consulta precisa ser medida com a **mesma régua** dos documentos.

```python
query_vector = vectorizer.transform(["gato peixe"])
# [[0.   0.   0.   0.61 0.   0.8 ]]
#   cach come dorme gato osso peixe
```

A consulta virou um vetor de 6 posições, as mesmas colunas da matriz. Agora ela pode ser comparada com cada linha.

Se usássemos `fit_transform` na consulta, criaríamos uma régua nova a partir dela:

```python
outro = TfidfVectorizer()
outro.fit_transform(["gato peixe"])
outro.get_feature_names_out()   # ['gato', 'peixe']  -> só 2 colunas
outro.idf_                      # [1. 1.]            -> todos os IDFs iguais
```

Dois problemas:

| Problema | Consequência |
|---|---|
| Vocabulário de 2 termos, e não 6 | O vetor da consulta tem 2 dimensões e a matriz tem 6. O cosseno não pode ser calculado, porque as colunas não correspondem. |
| IDF calculado com 1 documento | "gato" e "peixe" ficam com o mesmo peso (1,0). Some a informação de que "peixe" é mais raro que "gato" na coleção. |

Comparação com a matriz certa, usando `transform`: `peixe` pesa 0,8 e `gato` pesa 0,61.

Palavras que não existem na coleção são ignoradas:

```python
vectorizer.transform(["gato zebra"])
# [[0. 0. 0. 1. 0. 0.]]   -> "zebra" não está no vocabulário, só "gato" conta
```

Regra geral, vale para todo o scikit-learn:

| Método | Quando usar |
|---|---|
| `fit_transform` | **Uma vez**, nos dados de referência (a coleção). |
| `transform` | Em **qualquer coisa nova** que precise ficar no mesmo espaço (consultas, documentos novos). |

### Por que transformar em uma matriz

Computadores não calculam "parecido" entre textos, mas calculam entre números. A matriz é a forma de colocar todos os textos no mesmo sistema de coordenadas.

- **Cada coluna é um termo.** Cada documento é um ponto num espaço com uma dimensão por termo. A consulta é mais um ponto no mesmo espaço.
- **Só dá para comparar o que tem as mesmas colunas.** O cosseno multiplica posição por posição (`q_i × d_i`). Isso só faz sentido se a posição `i` significa o mesmo termo nos dois vetores.
- **Uma conta para todos.** `cosine_similarity(matrix, query_vector)` calcula a similaridade da consulta com todos os documentos de uma vez, sem laço em Python.
- **Serve para mais do que busca.** A mesma matriz permite comparar documentos entre si, agrupá-los e classificá-los.

```python
cosine_similarity(matrix, query_vector).flatten()
# [0.86, 0.37, 0.  ]  -> doc 0 é o mais parecido com "gato peixe"
```

Matriz esparsa: a maior parte dos valores é 0, porque cada documento usa poucos termos do vocabulário. O scikit-learn guarda só os valores diferentes de zero. Por isso `print(tfidf_matrix)` mostra linhas como `(0, 3) 0.52`, que significa documento 0, coluna 3 (`gato`), peso 0,52. Para ver a tabela completa, use `matrix.toarray()`.

Para explorar sozinho:

```python
print(vectorizer.get_feature_names_out())   # as colunas
print(vectorizer.idf_)                      # a "régua" de raridade
print(matrix.toarray().round(2))            # a matriz completa
```

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
