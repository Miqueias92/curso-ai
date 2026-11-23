# 05. Tokenização subword

## Motivação

As duas estratégias anteriores têm problemas opostos:

| | Vocabulário | Tamanho da sequência | OOV |
|---|---|---|---|
| Palavra | enorme | curto | sim |
| Caractere | minúsculo | longo | não |

**Subword** fica no meio: palavras frequentes viram um token só, e palavras raras são quebradas em pedaços reutilizáveis.

```
"lowest"  ->  ["low", "est</w>"]
"newer"   ->  ["ne", "w", "e", "r", "</w>"]
```

Palavras nunca vistas continuam representáveis, porque no pior caso viram caracteres. É a abordagem usada em BERT, GPT, LLaMA e na maioria dos LLMs atuais.

## Os três algoritmos principais

| Algoritmo | Ideia | Usado em |
|---|---|---|
| **BPE** (Byte Pair Encoding) | Parte dos caracteres e junta o par mais frequente, repetidamente. | GPT-2/3/4, LLaMA, RoBERTa |
| **WordPiece** | Parecido com BPE, mas escolhe a junção que mais aumenta a verossimilhança dos dados. Pedaços internos recebem prefixo `##`. | BERT |
| **Unigram** | Parte de um vocabulário grande e remove tokens que menos prejudicam a verossimilhança. | T5, ALBERT (via SentencePiece) |

## BPE passo a passo

1. Quebre cada palavra em caracteres e adicione um marcador de fim (`</w>`).
2. Conte os pares de símbolos vizinhos em todo o corpus.
3. Junte o par mais frequente em um novo símbolo. Essa junção é uma *merge*.
4. Repita os passos 2 e 3 `N` vezes. `N` define o tamanho do vocabulário.

Para tokenizar uma palavra nova, aplique as merges na mesma ordem em que foram aprendidas.

## Implementação do zero

Código completo em [`src/curso_ia/tokenization/bpe.py`](../src/curso_ia/tokenization/bpe.py). O núcleo:

```python
def _pair_counts(vocab):
    pairs = Counter()
    for symbols, freq in vocab.items():
        for pair in zip(symbols, symbols[1:]):
            pairs[pair] += freq
    return pairs

def train_bpe(corpus, num_merges):
    vocab = _build_vocab(corpus)
    merges = []
    for _ in range(num_merges):
        pairs = _pair_counts(vocab)
        if not pairs:
            break
        best = max(pairs, key=lambda p: (pairs[p], p))
        merges.append(best)
        vocab = {_merge(s, best): f for s, f in vocab.items()}
    return merges
```

Uso:

```python
from curso_ia.tokenization import bpe_encode, train_bpe

corpus = [
    "low low low low low",
    "lower lower",
    "newest newest newest newest newest newest",
    "widest widest widest",
]
merges = train_bpe(corpus, num_merges=10)
print(bpe_encode("lowest", merges))
```

Saída real:

```
merges aprendidas (em ordem):
 1. t + </w> -> t</w>
 2. s + t</w> -> st</w>
 3. e + st</w> -> est</w>
 4. o + w -> ow
 5. l + ow -> low
 6. w + est</w> -> west</w>
 7. n + e -> ne
 8. ne + west</w> -> newest</w>
 9. low + </w> -> low</w>
10. w + i -> wi

tokenizando palavras:
  lowest -> ['low', 'est</w>']
   newer -> ['ne', 'w', 'e', 'r', '</w>']
   wider -> ['wi', 'd', 'e', 'r', '</w>']
     low -> ['low</w>']
```

Observe que "lowest" nunca apareceu no corpus, mas foi montada com `low` e `est</w>`, dois pedaços aprendidos de outras palavras. Já "newer" ficou quase em caracteres, porque o corpus é pequeno e `er` nunca foi aprendido. Com um corpus real e milhares de merges, isso melhora.

Rodar: `uv run python examples/04_bpe.py`

## Limitações desta versão

- O corpus é minúsculo e a separação é só por espaço.
- Não há tratamento de bytes. O BPE do GPT-2 opera sobre bytes UTF-8, o que garante zero OOV para qualquer texto.
- É lento para corpora grandes. Bibliotecas reais usam implementações otimizadas.

## Bibliotecas para usar em projetos reais

Ainda não usadas neste repositório. Ficam como próximo passo do curso:

- [`tiktoken`](https://github.com/openai/tiktoken): tokenizador BPE da OpenAI.
- [`tokenizers`](https://github.com/huggingface/tokenizers) (Hugging Face): treina e usa BPE, WordPiece e Unigram.
- [`sentencepiece`](https://github.com/google/sentencepiece): BPE e Unigram sem depender de pré-tokenização por espaço.

Nota: o NLTK não implementa BPE, WordPiece nem Unigram.

## Referências

- [Sennrich et al. (2016): Neural Machine Translation of Rare Words with Subword Units (BPE)](https://arxiv.org/abs/1508.07909)
- [Wu et al. (2016): Google's Neural Machine Translation System (WordPiece)](https://arxiv.org/abs/1609.08144)
- [Kudo (2018): Subword Regularization (Unigram)](https://arxiv.org/abs/1804.10959)
- [Kudo & Richardson (2018): SentencePiece](https://arxiv.org/abs/1808.06226)
- [Hugging Face NLP Course, capítulo 6](https://huggingface.co/learn/nlp-course/chapter6/1)
- [Hugging Face: Summary of the tokenizers](https://huggingface.co/docs/transformers/tokenizer_summary)
- [Karpathy: Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE)
