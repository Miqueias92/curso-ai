# curso-ia

Repositório de estudos sobre IA, escrito para ser didático. Cada etapa do aprendizado tem uma documentação, código Python e exemplos executáveis.

## Trilha atual: tokenização

| # | Tema | Doc | Código | Exemplo |
|---|---|---|---|---|
| 1 | O que são tokens | [docs/01](docs/01-o-que-sao-tokens.md) | n/a | n/a |
| 2 | Por palavra | [docs/02](docs/02-tokenizacao-por-palavra.md) | [word.py](src/curso_ia/tokenization/word.py) | `examples/01_word.py` |
| 3 | Por caractere | [docs/03](docs/03-tokenizacao-por-caractere.md) | [char.py](src/curso_ia/tokenization/char.py) | `examples/02_char.py` |
| 4 | Por sentença | [docs/04](docs/04-tokenizacao-por-sentenca.md) | [sentence.py](src/curso_ia/tokenization/sentence.py) | `examples/03_sentence.py` |
| 5 | Subword (BPE do zero) | [docs/05](docs/05-tokenizacao-subword.md) | [bpe.py](src/curso_ia/tokenization/bpe.py) | `examples/04_bpe.py` |
| 6 | Comparação e escolha | [docs/06](docs/06-comparacao-e-escolha.md) | n/a | n/a |

Links de estudo: [docs/referencias.md](docs/referencias.md)

## Como rodar

Requer Python 3.11+ e [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python examples/01_word.py
uv run python examples/04_bpe.py
```

O NLTK baixa o modelo `punkt_tab` automaticamente na primeira execução.

## Estrutura

```
docs/                      # documentação de cada etapa
examples/                  # scripts executáveis
src/curso_ia/tokenization/ # implementações
```

## Próximas etapas

- Vocabulário e IDs
- Subword com `tiktoken` e `tokenizers`
- Embeddings
