# 07. Sistemas de recuperação de informação

## O que é

**Recuperação de informação** (*Information Retrieval*, IR) é o problema de encontrar, dentro de uma coleção grande de documentos, os que atendem a uma necessidade de informação do usuário. O exemplo mais conhecido é um buscador, mas o mesmo problema aparece em muitos outros lugares.

Vocabulário básico:

| Termo | Significado |
|---|---|
| **Coleção** (corpus) | Conjunto de documentos onde se busca. |
| **Documento** | Unidade recuperável: página, artigo, e-mail, chamado, trecho de PDF. |
| **Consulta** (*query*) | O que o usuário escreve para expressar o que procura. |
| **Relevância** | O quanto um documento atende à necessidade do usuário. |
| **Termo** | Token depois da tokenização e da normalização (ver [docs 01 a 06](01-o-que-sao-tokens.md)). |

A relevância é o ponto difícil. O usuário digita "banco" e pode querer uma instituição financeira ou um assento. O sistema só vê a consulta, não a intenção.

## Onde a tokenização entra

Todo modelo de recuperação clássico começa pelos tokens. O texto do documento e o texto da consulta passam pelo mesmo pipeline:

```
texto -> tokenização -> normalização -> termos
```

A normalização costuma incluir minúsculas, remoção de acentos (opcional), remoção de *stopwords* ("de", "a", "o") e *stemming* ou lematização ("aprendem" e "aprendizado" viram a mesma raiz). Se documento e consulta forem processados de formas diferentes, os termos não casam e a busca falha.

## Estrutura central: o índice invertido

Procurar uma palavra lendo todos os documentos a cada consulta é lento. Por isso se constrói, uma vez, um **índice invertido**: para cada termo, a lista dos documentos que o contêm.

Coleção de exemplo:

| Doc | Texto |
|---|---|
| D1 | machine learning aprende padrões com dados |
| D2 | banco de dados guarda dados de clientes |
| D3 | machine learning usa dados de clientes |
| D4 | redes neurais aprendem padrões |

Índice invertido (sem stopwords):

| Termo | Documentos (*postings*) |
|---|---|
| machine | D1, D3 |
| learning | D1, D3 |
| dados | D1, D2, D3 |
| clientes | D2, D3 |
| padrões | D1, D4 |
| banco | D2 |
| redes | D4 |

Para responder "dados", basta ler uma linha da tabela. Esta mesma coleção é usada nos próximos docs.

Índices reais costumam guardar, junto de cada documento, a frequência do termo e as posições. Isso é necessário para ranquear (docs 09 e 10) e para buscar frases exatas.

## Os três modelos desta trilha

| Modelo | Pergunta que responde | Resultado | Doc |
|---|---|---|---|
| **Booleano** | O documento satisfaz a expressão lógica? | Conjunto: casa ou não casa | [08](08-boolean-retrieval.md) |
| **Espaço vetorial** | Quão parecido o documento é da consulta? | Lista ranqueada por similaridade | [09](09-vector-space-model.md) |
| **Probabilístico** | Qual a chance de o documento ser relevante? | Lista ranqueada por probabilidade | [10](10-modelo-probabilistico.md) |

Os três são modelos **léxicos**: só casam termos que aparecem de fato no texto. Não entendem sinônimos ("carro" e "automóvel"). Essa é a principal limitação e o motivo de existirem a busca semântica com embeddings e os modelos híbridos, tema para etapas futuras.

## Como avaliar um sistema de busca

Para saber se um sistema é bom, compara-se o resultado com um conjunto de documentos que humanos marcaram como relevantes.

- **Precisão**: dos documentos retornados, que fração é relevante.
- **Revocação** (*recall*): dos documentos relevantes que existem, que fração foi retornada.

Exemplo: existem 10 documentos relevantes na coleção. O sistema retorna 8, e 6 deles são relevantes.

```
precisão  = 6 / 8  = 0,75
revocação = 6 / 10 = 0,60
```

Os dois puxam em direções opostas. Retornar tudo dá revocação 1,0 e precisão baixa. Retornar só um resultado certo dá precisão alta e revocação baixa.

Para listas ranqueadas, usam-se métricas que olham a posição, como **precisão@k**, **MAP** e **nDCG**.

## Onde aplicar

| Cenário | Modelo típico |
|---|---|
| Busca em biblioteca, base jurídica ou patentes, com consultas precisas | Booleano |
| Busca em site, documentação, e-commerce | BM25 (probabilístico), às vezes TF-IDF |
| Agrupar ou comparar documentos parecidos, detectar duplicatas | Espaço vetorial (TF-IDF e cosseno) |
| Filtros em bancos de dados e logs (`level:error AND service:api`) | Booleano |
| RAG: buscar trechos para dar contexto a um LLM | BM25, embeddings, ou os dois combinados |
| Sistema de suporte: achar chamados parecidos | TF-IDF ou BM25 |

## Referências

- [Manning, Raghavan, Schütze: Introduction to Information Retrieval (livro gratuito online)](https://nlp.stanford.edu/IR-book/)
- [Capítulo 1: Boolean retrieval e índice invertido](https://nlp.stanford.edu/IR-book/html/htmledition/boolean-retrieval-1.html)
- [Capítulo 8: Evaluation in information retrieval](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-in-information-retrieval-1.html)
