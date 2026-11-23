# 08. Boolean retrieval (recuperação booleana)

> **Pré-requisito:** este doc usa os conceitos de coleção, documento, termo e índice invertido, explicados no [doc 07: Sistemas de recuperação](07-sistemas-de-recuperacao.md). Se algum desses termos não estiver claro, leia o doc 07 primeiro.

## Ideia

É o modelo mais antigo e mais simples. A consulta é uma expressão lógica com os operadores `AND`, `OR` e `NOT`. Um documento ou satisfaz a expressão ou não satisfaz. Não existe "mais relevante" nem "menos relevante".

## Como funciona

Cada documento é tratado como um conjunto de termos. Cada termo tem uma lista de documentos (o índice invertido do [doc 07](07-sistemas-de-recuperacao.md)). Os operadores viram operações de conjuntos sobre essas listas:

| Operador | Operação | Efeito |
|---|---|---|
| `A AND B` | interseção | documentos que têm A e B |
| `A OR B` | união | documentos que têm A ou B |
| `NOT A` | complemento | todos os documentos que não têm A |

Também é comum representar como uma **matriz de incidência**, onde cada termo é um vetor de 0 e 1 com uma posição por documento. `AND`, `OR` e `NOT` viram operações bit a bit.

### A coleção de exemplo

Os exemplos abaixo usam esta coleção de 4 documentos (a mesma do [doc 07](07-sistemas-de-recuperacao.md)):

| Doc | Texto |
|---|---|
| D1 | machine learning aprende padrões com dados |
| D2 | banco de dados guarda dados de clientes |
| D3 | machine learning usa dados de clientes |
| D4 | redes neurais aprendem padrões |

### Como ler a matriz

- Cada **linha** é um termo.
- Cada **coluna** é um documento.
- **1** significa "o termo aparece nesse documento". **0** significa "não aparece".

Não é uma tabela verdade. Ela é um mapa de quais termos aparecem em quais documentos. A lógica entra quando você faz uma consulta: pega as linhas dos termos e combina coluna por coluna com AND, OR ou NOT. Por exemplo, a linha `dados | 1 1 1 0` diz que "dados" aparece em D1, D2 e D3, e não aparece em D4.

Matriz da coleção acima (mostrando só alguns termos):

| Termo | D1 | D2 | D3 | D4 |
|---|---|---|---|---|
| machine | 1 | 0 | 1 | 0 |
| learning | 1 | 0 | 1 | 0 |
| dados | 1 | 1 | 1 | 0 |
| clientes | 0 | 1 | 1 | 0 |
| padrões | 1 | 0 | 0 | 1 |
| banco | 0 | 1 | 0 | 0 |

## Exemplos com a coleção do doc 07

**Consulta 1:** `machine AND dados AND NOT clientes`

```
machine   = 1 0 1 0
dados     = 1 1 1 0
NOT clientes = 1 0 0 1     (clientes = 0 1 1 0)

AND dos três = 1 0 0 0   ->  D1
```

Resultado: {D1}. O D3 tem machine e dados, mas é excluído porque contém "clientes".

**Consulta 2:** `padrões OR clientes`

```
padrões  = 1 0 0 1
clientes = 0 1 1 0
OR       = 1 1 1 1   ->  D1, D2, D3, D4
```

Resultado: todos os documentos. Um `OR` aberto tende a retornar muito.

**Consulta 3:** `banco AND learning`

```
banco    = 0 1 0 0
learning = 1 0 1 0
AND      = 0 0 0 0   ->  nenhum documento
```

Resultado vazio. Esse é o comportamento típico de um `AND` muito restritivo.

## Otimização: ordem de processamento

Em consultas com vários `AND`, começa-se pelos termos com a lista menor. Para `banco AND dados AND machine`, a lista de "banco" (1 documento) é cruzada primeiro. Isso reduz o trabalho porque a interseção nunca será maior que a menor lista.

## Vantagens

- Controle total: o usuário sabe exatamente por que um documento foi retornado.
- Resultados previsíveis e reproduzíveis.
- Muito rápido, só envolve operações de conjunto.
- Fácil de combinar com filtros estruturados (data, autor, categoria).

## Limitações

- **Sem ranking.** Todos os resultados valem o mesmo. Um documento que cita o termo uma vez fica igual ao que trata do assunto por inteiro.
- **Tudo ou nada.** `AND` demais retorna zero resultados, `OR` demais retorna milhares. É difícil acertar o ponto.
- **Exige conhecimento do usuário.** Escrever boas expressões lógicas é uma habilidade.
- **Sem tolerância.** Um documento que casa 2 de 3 termos de um `AND` não aparece.

Essas limitações motivam o [modelo de espaço vetorial](09-vector-space-model.md), que ordena os resultados.

## Onde aplicar

- **Busca profissional:** bibliotecas, revisões sistemáticas em saúde (PubMed), pesquisa jurídica e de patentes. Pesquisadores querem controle e reprodutibilidade, e documentam a consulta exata usada.
- **Filtros em sistemas:** consultas em logs, SIEM, bancos de dados e e-commerce (`categoria = tênis AND tamanho = 42 AND NOT esgotado`).
- **E-mail e arquivos:** `from:ana AND has:anexo NOT label:spam`.
- **Primeira etapa de um pipeline:** o booleano reduz a coleção a candidatos, e outro modelo ranqueia só esses.
- **Compliance e e-discovery:** onde é preciso provar que uma busca foi completa e repetível.

## Referências

- [Manning et al.: Boolean retrieval](https://nlp.stanford.edu/IR-book/html/htmledition/boolean-retrieval-1.html)
- [Manning et al.: Processing Boolean queries](https://nlp.stanford.edu/IR-book/html/htmledition/processing-boolean-queries-1.html)
- [PubMed: guia de busca (exemplo real de consultas booleanas)](https://pubmed.ncbi.nlm.nih.gov/help/)
