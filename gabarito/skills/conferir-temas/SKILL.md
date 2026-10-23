---
name: conferir-temas
description: Confere se o autor de uma ação de medicamento cumpriu os requisitos do Tema 6 do STF e qual é a competência pelo Tema 1234, lendo os PDFs do caso, e entrega um relatório em Word. Use quando o usuário pedir para conferir um caso de medicamento nos Temas 6 e 1234.
---

# Conferir os Temas 6 e 1234

Entrada: uma pasta de caso com os PDFs dos autos e, na pasta `temas/`, os arquivos `tema-6-stf.md` e `tema-1234-stf.md`.
Saída: `relatorio.docx` na pasta do caso, feito a partir de um `caso.json`.

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
   - Negativa administrativa (a): ofício, protocolo ou resposta escrita é prova; só a frase "o pedido foi negado" na inicial é alegação.
   - Evidência de alto nível (d): só ensaio clínico randomizado, revisão sistemática ou meta-análise contam. Citar "estudos" ou diretrizes, sem apontar o estudo, é `nao_comprovado`.
   - Incapacidade financeira (f): com advogado particular, exige prova (renda, CadÚnico, declaração com documentos); com Defensoria Pública, é `dispensado`.
   - Competência (Tema 1234): compare o valor anual do tratamento com 210 salários mínimos. Use o valor que os autos mostram e diga que o usuário deve conferir o PMVG na lista CMED e o salário mínimo vigente. Se os autos não dizem, escreva "conferir".
5. Rode `python3 relatorio.py caso.json logo-escritorio.png relatorio.docx` (precisa de `python-docx`: `pip install python-docx`). O `relatorio.py` e o logo vêm junto com esta skill.
6. Termine dizendo, em poucas linhas, o que o usuário deve conferir à mão: as páginas decisivas e qualquer PDF que não foi possível ler.

Este relatório organiza a leitura. A decisão sobre a defesa é do procurador.
