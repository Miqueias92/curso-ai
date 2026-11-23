# 09. Vector space model (modelo de espaço vetorial)

## Ideia

Proposto por Gerard Salton nos anos 1970 (sistema SMART). Cada documento e cada consulta é representado como um **vetor**, com uma dimensão por termo do vocabulário. A relevância passa a ser a **proximidade** entre o vetor da consulta e o vetor do documento. O resultado é uma lista **ranqueada**, e não mais um conjunto.

Isso resolve o principal problema do [modelo booleano](08-boolean-retrieval.md): documentos que casam parcialmente com a consulta aparecem, e os que casam melhor aparecem primeiro.

## Passo 1: pesos dos termos

Marcar apenas 0 ou 1 (o termo está ou não está) perde informação. Dois fatores melhoram isso.

**TF (*term frequency*):** quantas vezes o termo aparece no documento. Um documento que repete "vacina" dez vezes provavelmente trata mais do assunto que um que cita uma vez.

**IDF (*inverse document frequency*):** o quão raro o termo é na coleção. Uma palavra que aparece em quase todos os documentos ("dados", numa base de dados) diferencia pouco. Uma palavra rara diferencia muito.

```
idf(t) = log( N / df(t) )

N     = número total de documentos
df(t) = número de documentos que contêm o termo t
```

O peso final é o produto:

```
peso(t, d) = tf(t, d) × idf(t)
```

Variações comuns de TF: contagem bruta, `1 + log(tf)` (suaviza repetições), e normalização pelo tamanho do documento. Todas tentam evitar que um termo repetido 100 vezes valha 100 vezes mais.

## Passo 2: similaridade do cosseno

Com os vetores prontos, mede-se o ângulo entre eles:

```
                 q · d              Σ q_i × d_i
cos(q, d) = ──────────────── = ─────────────────────
              ‖q‖ × ‖d‖        √Σ q_i²  ×  √Σ d_i²
```

O valor vai de 0 (nenhum termo em comum) a 1 (mesma direção). Usar o ângulo, e não a distância, evita favorecer documentos longos: um documento duplicado dentro dele mesmo tem a mesma direção e a mesma similaridade.

## Exemplo completo à mão

Coleção com N = 3 documentos:

| Doc | Texto |
|---|---|
| D1 | gato come peixe |
| D2 | gato dorme |
| D3 | cachorro come osso |

**Consulta:** `gato peixe`

**IDF** (usando log base 10):

| Termo | df | idf = log10(3/df) |
|---|---|---|
| gato | 2 | 0,176 |
| come | 2 | 0,176 |
| peixe | 1 | 0,477 |
| dorme | 1 | 0,477 |
| cachorro | 1 | 0,477 |
| osso | 1 | 0,477 |

**Vetores TF-IDF** (todos os termos aparecem uma vez, então tf = 1):

| | gato | come | peixe | dorme | cachorro | osso | norma |
|---|---|---|---|---|---|---|---|
| D1 | 0,176 | 0,176 | 0,477 | 0 | 0 | 0 | 0,538 |
| D2 | 0,176 | 0 | 0 | 0,477 | 0 | 0 | 0,509 |
| D3 | 0 | 0,176 | 0 | 0 | 0,477 | 0,477 | 0,697 |
| Consulta | 0,176 | 0 | 0,477 | 0 | 0 | 0 | 0,509 |

**Cossenos:**

```
cos(q, D1) = (0,176×0,176 + 0,477×0,477) / (0,509 × 0,538) = 0,2585 / 0,2736 ≈ 0,94
cos(q, D2) = (0,176×0,176)               / (0,509 × 0,509) = 0,0310 / 0,2586 ≈ 0,12
cos(q, D3) = 0                                                               =  0
```

**Ranking final:** D1 (0,94), D2 (0,12), D3 (0).

Leitura do resultado:
- D1 vence porque contém "gato" e "peixe", e "peixe" é um termo raro (alto IDF).
- D2 contém só "gato", que é comum, então a pontuação é baixa.
- D3 não tem nenhum termo da consulta.

Um modelo booleano com `gato OR peixe` retornaria D1 e D2 sem dizer qual é melhor.

## Vantagens

- Ranking natural, com pontuação numérica.
- Aceita consultas em linguagem natural, sem operadores.
- Simples de implementar e de explicar.
- O mesmo vetor serve para outras tarefas: **comparar documentos entre si**, agrupar (*clustering*), classificar.

## Limitações

- **Termos independentes.** Cada dimensão é tratada isoladamente, então "banco de dados" e "dados de banco" ficam iguais.
- **Casamento léxico.** "carro" e "automóvel" são dimensões diferentes, sem relação.
- **Vetores enormes e esparsos.** Uma dimensão por termo do vocabulário, quase todas com zero.
- **Pesos heurísticos.** TF-IDF funciona bem na prática, mas não tem uma justificativa teórica de probabilidade. Isso é abordado no [modelo probabilístico](10-modelo-probabilistico.md).
- **Viés de tamanho.** A normalização ajuda, mas documentos muito longos ou muito curtos ainda são tratados de forma imperfeita.

## Onde aplicar

- **Busca em sites e documentações pequenas ou médias**, quando um baseline simples é suficiente.
- **Detecção de duplicatas e plágio:** comparar o cosseno entre documentos.
- **Sistemas de recomendação por conteúdo:** artigos parecidos com o que o usuário leu.
- **Agrupamento de textos:** chamados de suporte, avaliações, notícias.
- **Extração de palavras-chave:** os termos de maior TF-IDF de um documento o descrevem bem.
- **Ponte para embeddings:** a ideia de "documento como vetor, relevância como proximidade" é a mesma da busca semântica. A diferença é que os vetores densos aprendidos capturam significado, e não só palavras.

## Referências

- [Manning et al.: The vector space model for scoring](https://nlp.stanford.edu/IR-book/html/htmledition/the-vector-space-model-for-scoring-1.html)
- [Manning et al.: Inverse document frequency](https://nlp.stanford.edu/IR-book/html/htmledition/inverse-document-frequency-1.html)
- [Manning et al.: Tf-idf weighting](https://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-weighting-1.html)
- [Salton, Wong, Yang (1975): A Vector Space Model for Automatic Indexing](https://dl.acm.org/doi/10.1145/361219.361220)
- [Spärck Jones (1972): A statistical interpretation of term specificity (origem do IDF)](https://www.emerald.com/insight/content/doi/10.1108/eb026526/full/html)
