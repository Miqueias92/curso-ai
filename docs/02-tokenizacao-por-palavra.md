# 02. Tokenização por palavra

## Ideia

Divide o texto em palavras e pontuações. É a forma mais intuitiva e foi o padrão por muito tempo em NLP clássico.

```
"Machine learning é legal."  ->  ["Machine", "learning", "é", "legal", "."]
```

## Implementação

Usamos o NLTK. Código completo em [`src/curso_ia/tokenization/word.py`](../src/curso_ia/tokenization/word.py).

```python
import nltk

nltk.download("punkt_tab")  # modelo necessário, baixado uma vez

text = "Machine learning é um campo da inteligência artificial."
print(nltk.word_tokenize(text))
```

## Pré-processamento

Em geral o texto é normalizado antes de virar tokens:

```python
from curso_ia.tokenization import preprocess

text = "Machine learning é um campo da inteligência artificial que permite que computadores aprendam padrões a partir de dados."

preprocess(text)                    # minúsculas e sem pontuação
preprocess(text, only_alnum=False)  # minúsculas, mantendo pontuação
```

Saída real de `preprocess(text)`:

```
['machine', 'learning', 'é', 'um', 'campo', 'da', 'inteligência', 'artificial',
 'que', 'permite', 'que', 'computadores', 'aprendam', 'padrões', 'a', 'partir', 'de', 'dados']
```

O filtro `word.isalnum()` remove tokens como `"."` e `","`. Use quando a pontuação não importa para sua tarefa (por exemplo, contagem de palavras). Mantenha a pontuação quando ela carrega significado (por exemplo, análise de sentimento com "!!!").

Rodar: `uv run python examples/01_word.py`

## Vantagens

- Tokens têm significado direto, fáceis de ler e depurar.
- Sequências curtas.

## Limitações

- **Vocabulário enorme:** "casa", "casas", "casinha" e "casarão" são tokens independentes.
- **OOV:** uma palavra nunca vista (um erro de digitação, um nome novo) não tem representação.
- **Línguas sem espaço** (chinês, japonês) não funcionam bem com divisão por espaço.

Essas limitações motivam a tokenização por [caractere](03-tokenizacao-por-caractere.md) e por [subword](05-tokenizacao-subword.md).

## Referências

- [NLTK: módulo tokenize](https://www.nltk.org/api/nltk.tokenize.html)
- [NLTK Book, capítulo 3: Processing Raw Text](https://www.nltk.org/book/ch03.html)
