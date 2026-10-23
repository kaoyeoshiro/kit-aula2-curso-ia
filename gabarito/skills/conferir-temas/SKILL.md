---
name: conferir-temas
description: Confere se o autor de uma ação de medicamento cumpriu os requisitos do Tema 6 do STF e qual é a competência pelo Tema 1234, lendo os PDFs do caso, e entrega um relatório em Word. Use quando o usuário pedir para conferir um caso de medicamento nos Temas 6 e 1234.
---

# Conferir os Temas 6 e 1234

Entrada: uma pasta de caso com os PDFs dos autos e, na pasta `temas/`, os arquivos `tema-6-stf.md` e `tema-1234-stf.md`.
Saída: `saida/caso-N/caso.json` e `saida/caso-N/relatorio.docx` (crie a pasta `saida/` ao lado de `casos/`; não grave nada dentro de `casos/`).

## Passos

1. Leia `temas/tema-6-stf.md` e `temas/tema-1234-stf.md`. Eles são a única fonte dos requisitos.
2. Leia todos os PDFs do caso. Se algum for digitalizado (sem texto), diga qual e leia as imagens; se não conseguir ler, diga que não conseguiu.
3. Crie o `caso.json` com o formato de `exemplo.json` (ao lado desta skill). Para cada requisito (a) a (f) do Tema 6, escolha uma situação:
   - `atendido`: o autor juntou prova do requisito.
   - `nao_comprovado`: o autor alega, mas não há prova nos autos.
   - `nao_encontrado`: nem alegação nem prova nos autos.
   - `dispensado`: só para (f), quando o autor é representado pela Defensoria Pública.
   Em "onde", escreva o nome do arquivo e a página (por exemplo, "02-laudo-medico.pdf, p. 1"). Em "obs", uma frase com o motivo.
4. Regras fixas:
   - Se não achar, diga "não encontrei". Nunca complete por conta própria.
   - Negativa administrativa (a): é prova a resposta escrita que nega (ofício, declaração, resposta da Secretaria). Protocolo de pedido sem resposta só prova que o pedido foi feito: é `nao_comprovado`. A frase "o pedido foi negado" na inicial, sem documento, também.
   - Conitec (b): a inicial precisa tratar da não incorporação, do pedido de incorporação ou da demora. Se ela não trata, é `nao_encontrado`. Se outro documento (por exemplo o NATJus) registra um fato sobre a Conitec, como pedido em análise ou ausência de pedido, cite na observação e escreva que o usuário deve conferir.
   - Medicamento já nas listas do SUS (RENAME, RESME, REMUME): o Tema 6 trata de medicamento não incorporado. Avise isso no início da conclusão (a discussão é de enquadramento no protocolo clínico), marque (b) como `nao_encontrado` e explique na observação.
   - Substituição (c): só é `atendido` se o laudo explica por que cada alternativa do SUS não serve. Afirmar "não há substituto", sem explicar, ou haver alternativa apontada pelo NATJus, é `nao_comprovado`.
   - Evidência de alto nível (d): só ensaio clínico randomizado, revisão sistemática ou meta-análise contam, e precisam estar nos autos ou ser descritos com o resultado. Citar "estudos" ou diretrizes, ou apenas nomear o ensaio no laudo, sem juntá-lo, é `nao_comprovado`.
   - Imprescindibilidade (e): exige laudo médico fundamentado que descreva o tratamento já realizado. O questionário ajuda, mas o que o tema pede é o laudo.
   - Incapacidade financeira (f): com advogado particular, exige prova (renda, CadÚnico, declaração com documentos); com Defensoria Pública, é `dispensado`.
   - Competência (Tema 1234): compare o valor anual do tratamento com 210 salários mínimos. Use o valor que os autos mostram e diga que o usuário deve conferir o PMVG na lista CMED e o salário mínimo vigente. Se os autos não dizem, escreva "conferir".
5. Gere o Word com o `relatorio.py` e o `logo-escritorio.png` que estão na pasta desta skill. Precisa da biblioteca `python-docx`. Se `python3 -c "import docx"` der erro, crie um ambiente virtual e use o Python dele:
   `python3 -m venv .venv && .venv/bin/pip install python-docx` (no Windows, `.venv\Scripts\pip`).
   Comando (com o Python do ambiente virtual, se você criou um: `.venv/bin/python`): `python3 relatorio.py saida/caso-N/caso.json logo-escritorio.png saida/caso-N/relatorio.docx`, com os caminhos completos de `relatorio.py` e do logo.
6. Termine dizendo, em poucas linhas, o que o usuário deve conferir à mão: as páginas decisivas e qualquer PDF que não foi possível ler.

Este relatório organiza a leitura. A decisão sobre a defesa é do procurador.
