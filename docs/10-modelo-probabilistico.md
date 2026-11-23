# 10. Probabilistic retrieval model (modelo probabilístico)

## Ideia

Em vez de medir "semelhança", o modelo probabilístico tenta estimar a **probabilidade de um documento ser relevante** para uma consulta:

```
P(relevante | documento, consulta)
```

e ordena os documentos por essa probabilidade. A base teórica é o **Princípio do Ranqueamento Probabilístico** (Robertson, 1977): se os documentos são ordenados pela probabilidade de relevância, o sistema entrega o melhor resultado possível dado a informação disponível.

A diferença para o [espaço vetorial](09-vector-space-model.md) é de fundamento. O TF-IDF é uma heurística que funciona. O modelo probabilístico parte de uma hipótese sobre o que torna um documento relevante e deriva a fórmula de pesos a partir dela.

## Primeira versão: Binary Independence Model (BIM)

O BIM (Robertson e Spärck Jones, 1976) faz duas suposições simplificadoras:

1. **Binário:** cada termo está presente ou ausente no documento (sem contar frequência).
2. **Independência:** os termos ocorrem independentemente uns dos outros.

Para cada termo `t`, define-se:

- `p_t` = probabilidade de o termo aparecer em um documento **relevante**.
- `u_t` = probabilidade de o termo aparecer em um documento **não relevante**.

Se um termo é bem mais provável em documentos relevantes do que nos demais, ele é um bom indicador. O peso do termo é:

```
c_t = log [ p_t (1 − u_t) / ( u_t (1 − p_t) ) ]
```

e a pontuação do documento é a soma de `c_t` sobre os termos da consulta que ele contém.

Sem exemplos de documentos relevantes (o caso normal, no início), assume-se `p_t = 0,5` e estima-se `u_t` pelo `df`. O peso resultante é parecido com um IDF:

```
c_t ≈ log( (N − df_t) / df_t )
```

Ou seja, o IDF aparece como consequência do modelo, e não como uma escolha.

### Exemplo

Coleção de N = 100 documentos. Consulta: `vacina gripe`.

| Termo | df | peso aproximado `log10((N−df)/df)` |
|---|---|---|
| vacina | 5 | log10(95/5) = 1,28 |
| gripe | 50 | log10(50/50) = 0,00 |

"Gripe" aparece na metade dos documentos, então não ajuda a separar relevantes de não relevantes, e o peso é zero. "Vacina" é rara e recebe um peso alto. Um documento com os dois termos vale 1,28; um só com "vacina" também vale 1,28; um só com "gripe" vale 0.

## Evolução: o BM25

O BIM ignora a frequência do termo e o tamanho do documento. O **BM25** (*Best Match 25*), desenvolvido por Robertson, Walker e colegas nos anos 1990 (sistema Okapi), corrige isso mantendo a base probabilística. É até hoje um dos métodos mais fortes e usados da área.

```
                            f(t,d) × (k1 + 1)
score(d, q) = Σ  idf(t) × ─────────────────────────────────────
              t∈q            f(t,d) + k1 × (1 − b + b × |d| / avgdl)

f(t,d) = frequência do termo t no documento d
|d|    = tamanho do documento (em termos)
avgdl  = tamanho médio dos documentos da coleção
k1, b  = parâmetros ajustáveis (valores comuns: k1 = 1,2 e b = 0,75)
```

O IDF usado na prática (por exemplo, no Lucene) é:

```
idf(t) = ln( 1 + (N − df + 0,5) / (df + 0,5) )
```

### Duas ideias centrais do BM25

**1. Saturação da frequência do termo.** No TF-IDF, repetir uma palavra 20 vezes vale quase 20 vezes mais do que uma. No BM25, o ganho diminui e tende a um teto. Com `k1 = 1,2` e um documento de tamanho médio, a parte do termo vale:

| Ocorrências (f) | Valor da fração |
|---|---|
| 1 | 1,00 |
| 2 | 1,38 |
| 5 | 1,77 |
| 10 | 1,96 |
| ∞ | 2,20 (teto = k1 + 1) |

Depois de umas poucas ocorrências, repetir o termo quase não muda a nota. Isso torna o ranking mais resistente a textos que repetem palavras para enganar a busca (*keyword stuffing*).

**2. Normalização pelo tamanho do documento.** O parâmetro `b` controla o quanto o tamanho penaliza. Para um termo que aparece 2 vezes, com `k1 = 1,2` e `b = 0,75`:

| Tamanho do documento | Valor da fração |
|---|---|
| metade da média | 1,60 |
| igual à média | 1,38 |
| o dobro da média | 1,07 |

O mesmo número de ocorrências vale mais num documento curto, porque ele é mais concentrado no assunto. Um documento longo tem mais chance de citar o termo por acaso.

### Efeito dos parâmetros

| Parâmetro | Valor baixo | Valor alto |
|---|---|---|
| `k1` | saturação rápida, a frequência importa pouco | saturação lenta, a frequência importa mais |
| `b` | 0 = ignora o tamanho do documento | 1 = normalização total pelo tamanho |

Os valores padrão (1,2 e 0,75) funcionam bem na maioria dos casos. Ajuste com um conjunto de consultas avaliadas, não "no olho".

## Comparação dos três modelos

| | Booleano | Espaço vetorial (TF-IDF) | Probabilístico (BM25) |
|---|---|---|---|
| Saída | conjunto | ranking | ranking |
| Consulta | expressão lógica | texto livre | texto livre |
| Casamento parcial | não | sim | sim |
| Usa frequência do termo | não | sim | sim, com saturação |
| Considera tamanho do documento | não | pela normalização do vetor | sim, com parâmetro `b` |
| Fundamento | lógica de conjuntos | geometria | probabilidade |
| Parâmetros | nenhum | escolha da variação de TF e IDF | `k1`, `b` |

## Limitações

- **Casamento léxico.** Como os outros dois, não entende sinônimos nem contexto.
- **Independência dos termos.** A ordem das palavras é ignorada.
- **Sem dados de relevância, as probabilidades são estimadas por suposição.** O BM25 contorna isso com o IDF.
- **Parâmetros dependem da coleção.** Textos curtos (títulos) e longos (artigos) se comportam de modo diferente.

## Onde aplicar

- **Motores de busca de uso geral:** Elasticsearch, OpenSearch, Apache Solr e Lucene usam BM25 como pontuação padrão.
- **Busca em e-commerce, documentação, bases de conhecimento e suporte.**
- **RAG:** a etapa de recuperação costuma combinar BM25 (bom para nomes, códigos e termos exatos) com busca por embeddings (bom para significado). Essa combinação se chama **busca híbrida**.
- **Baseline de avaliação:** antes de adotar um modelo neural, compara-se com BM25. Em vários conjuntos de dados ele continua difícil de superar.

## Referências

- [Manning et al.: The Probability Ranking Principle](https://nlp.stanford.edu/IR-book/html/htmledition/the-probability-ranking-principle-1.html)
- [Manning et al.: The Binary Independence Model](https://nlp.stanford.edu/IR-book/html/htmledition/the-binary-independence-model-1.html)
- [Manning et al.: Okapi BM25](https://nlp.stanford.edu/IR-book/html/htmledition/okapi-bm25-a-non-binary-model-1.html)
- [Robertson e Zaragoza (2009): The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf)
- [Robertson e Spärck Jones (1976): Relevance weighting of search terms](https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.4630270302)
- [Elasticsearch: Practical BM25 (artigo sobre o ajuste de k1 e b)](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables)
