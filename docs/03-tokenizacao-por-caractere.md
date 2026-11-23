# 03. Tokenização por caractere

## Ideia

Cada caractere é um token.

```
"Olá, IA!"  ->  ['O', 'l', 'á', ',', ' ', 'I', 'A', '!']
```

## Implementação

Em Python, uma `str` já é iterável por caractere. Código em [`src/curso_ia/tokenization/char.py`](../src/curso_ia/tokenization/char.py).

```python
def char_tokenize(text: str) -> list[str]:
    return list(text)

tokens = char_tokenize("Olá, IA!")
print(tokens)
print("vocabulário:", sorted(set(tokens)))
```

Saída real:

```
['O', 'l', 'á', ',', ' ', 'I', 'A', '!']
8 caracteres -> 8 tokens
vocabulário: [' ', '!', ',', 'A', 'I', 'O', 'l', 'á']
```

Rodar: `uv run python examples/02_char.py`

## Vantagens

- **Vocabulário pequeno:** algumas centenas de símbolos cobrem uma língua.
- **Sem OOV:** qualquer palavra, inclusive erros de digitação, é representável.

## Limitações

- **Sequências longas:** um texto de 1000 caracteres vira 1000 tokens, o que torna o modelo mais lento e consome a janela de contexto.
- **Pouco significado por token:** o modelo precisa aprender que `c`, `a`, `s`, `a` juntos formam "casa".

## Observação sobre Unicode

`list(text)` separa por *code point*. Letras acentuadas escritas em forma decomposta (`a` + acento combinante) podem virar dois tokens. Normalize antes, se necessário:

```python
import unicodedata

text = unicodedata.normalize("NFC", text)
```

Existe também a tokenização por **byte** (UTF-8), com vocabulário fixo de 256 valores. Ela é a base do BPE usado em modelos como o GPT (ver [05](05-tokenizacao-subword.md)).

## Referências

- [Python: unicodedata](https://docs.python.org/3/library/unicodedata.html)
- [Unicode Normalization Forms (UAX #15)](https://unicode.org/reports/tr15/)
