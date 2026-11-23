# 01. O que são tokens

## Definição

Um **token** é a menor unidade de texto que um modelo de linguagem processa. **Tokenização** é o processo de quebrar um texto em tokens. Esses tokens podem ser palavras, pedaços de palavras, caracteres ou sentenças, dependendo da estratégia.

Modelos não leem texto, leem números. O caminho completo é:

```
texto  ->  tokens  ->  IDs (números)  ->  embeddings (vetores)  ->  modelo
"gato" ->  ["gato"] -> [4821]          -> [0.12, -0.8, ...]
```

Este repositório cobre o primeiro passo: texto para tokens.

## Por que isso importa

- **Vocabulário:** o conjunto de tokens distintos que o modelo conhece. Um vocabulário grande aumenta memória e custo. Um pequeno gera sequências longas.
- **Tamanho da sequência:** modelos têm limite de tokens de entrada (a "janela de contexto"). Mais tokens por texto significa menos texto cabendo no contexto.
- **Custo:** APIs de LLM cobram por token.
- **Palavras desconhecidas (OOV, *out of vocabulary*):** se o texto tem algo que não está no vocabulário, o modelo precisa de um plano para lidar com isso.

## Token não é palavra

Uma palavra pode virar vários tokens, e um token pode ser só parte de uma palavra. Em português, "inteligência" costuma ser dividida em mais de um token nos modelos modernos. Isso varia conforme o tokenizador.

## Estratégias vistas neste repositório

| Estratégia | Unidade | Doc |
|---|---|---|
| Palavra | palavras e pontuação | [02](02-tokenizacao-por-palavra.md) |
| Caractere | cada caractere | [03](03-tokenizacao-por-caractere.md) |
| Sentença | frases | [04](04-tokenizacao-por-sentenca.md) |
| Subword | pedaços de palavra | [05](05-tokenizacao-subword.md) |

A comparação final está em [06](06-comparacao-e-escolha.md).

## Referências

- [Hugging Face: Summary of the tokenizers](https://huggingface.co/docs/transformers/tokenizer_summary)
- [OpenAI Tokenizer (visualizador online)](https://platform.openai.com/tokenizer)
- [Andrej Karpathy: Let's build the GPT Tokenizer (vídeo)](https://www.youtube.com/watch?v=zduSFxRajkE)
