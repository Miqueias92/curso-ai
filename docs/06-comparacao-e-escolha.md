# 06. Comparação e escolha

## Tabela comparativa

| Estratégia | Vocabulário | Sequência | OOV | Bom para |
|---|---|---|---|---|
| Palavra | muito grande | curta | sim | NLP clássico, bag-of-words, TF-IDF |
| Caractere | muito pequeno | muito longa | não | idiomas com muita variação, correção ortográfica |
| Sentença | ilimitado | n/a | n/a | dividir documentos, chunking, tradução |
| Subword | médio (30k a 100k) | média | praticamente não | modelos de linguagem modernos |

## Como escolher

- Vai alimentar um **LLM ou Transformer**? Use o tokenizador do próprio modelo (subword). Trocar de tokenizador exige retreinar o modelo.
- Vai fazer **contagem de palavras, TF-IDF ou busca simples**? Palavra com pré-processamento.
- Precisa **dividir documentos grandes**? Sentença, e depois palavra ou subword em cada parte.
- Texto muito ruidoso ou sem espaços? Caractere ou byte.

## Resumo do pipeline

```
documento -> sentenças -> (normalização) -> tokens -> IDs -> modelo
```

## Próximos passos do curso

- Converter tokens em IDs e montar um vocabulário.
- Testar `tiktoken` e `tokenizers` e comparar com o BPE do zero.
- Embeddings.

## Referências

Veja [referencias.md](referencias.md).
