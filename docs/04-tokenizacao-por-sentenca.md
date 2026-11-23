# 04. Tokenização por sentença

## Ideia

Divide o texto em frases. Cada sentença é uma unidade. Esta etapa raramente é a entrada final de um modelo. Ela costuma ser a primeira etapa do pipeline: separar frases e depois tokenizar cada uma por palavra ou subword.

```
"Eu gosto de IA. Você também?"  ->  ["Eu gosto de IA.", "Você também?"]
```

## Por que não é só `split(".")`

O ponto aparece em abreviações ("Dr."), números ("3.14") e reticências. O `sent_tokenize` do NLTK usa o algoritmo **Punkt**, que aprende quais pontos encerram uma frase.

## Implementação

Código em [`src/curso_ia/tokenization/sentence.py`](../src/curso_ia/tokenization/sentence.py).

```python
import nltk

nltk.download("punkt_tab")

text = (
    "Machine learning é um campo da inteligência artificial. "
    "O Dr. Silva estuda o tema desde 2010. "
    "Sem serem programados explicitamente, os computadores aprendem com dados."
)

for sentence in nltk.sent_tokenize(text, language="portuguese"):
    print(sentence)
```

Saída real:

```
1: Machine learning é um campo da inteligência artificial.
2: O Dr. Silva estuda o tema desde 2010.
3: Sem serem programados explicitamente, os computadores aprendem com dados.
```

O "Dr." não encerrou a frase. Um `split(".")` teria cortado ali.

Rodar: `uv run python examples/03_sentence.py`

## Usos comuns

- Dividir documentos longos em partes (*chunking*) para busca e RAG.
- Resumo e tradução, que trabalham frase a frase.
- Primeiro passo antes da tokenização por palavra.

## Limitações

- Depende de idioma e de pontuação correta. Textos de redes sociais, sem pontuação, falham.
- Uma sentença é longa e variável demais para ser um token de modelo.

## Referências

- [Kiss & Strunk (2006): Unsupervised Multilingual Sentence Boundary Detection (Punkt)](https://aclanthology.org/J06-4003/)
- [NLTK: sent_tokenize](https://www.nltk.org/api/nltk.tokenize.html)
