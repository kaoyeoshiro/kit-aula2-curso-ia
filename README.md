# Kit da Aula 2: conferir os Temas 6 e 1234 do STF

Seis casos de medicamento, todos fictícios (recriados a partir de situações reais, sem nenhum dado verdadeiro).
O escritório (Dias & Moura) também é fictício.

## O que tem aqui

- `casos/`: os autos de cada caso em PDF (petição inicial, laudo, receita e o que mais importa).
- `temas/`: o texto dos Temas 6 e 1234 em Markdown, com fonte e data da consulta.
- `escritorio/`: o logo do escritório, usado no relatório.
- `gabarito/`: o relatório pronto de cada caso, a resposta (`gabarito.json`) e a skill `conferir-temas`.
  Só abra depois de tentar a sua.

## Como usar na aula

1. Baixe o kit: botão verde **Code** > **Download ZIP**, e extraia a pasta.
2. Abra a pasta no seu app (Claude, ChatGPT Work ou Codex).
3. Escolha um caso e peça ao agente que confira, com os temas, se o autor cumpriu os requisitos do Tema 6 e qual é a
   competência pelo Tema 1234. Use os seis elementos do pedido e a regra "se não souber, diga".
4. Instale a skill `conferir-temas` (copie a pasta `gabarito/skills/conferir-temas` para a pasta de skills da sua
   ferramenta, ou envie o arquivo `gabarito/conferir-temas.zip` no app do Claude) e rode no caso 2, para ver o
   relatório em Word.
5. Grave o que o agente gerar em `saida/caso-N/`, não dentro de `casos/`.
6. Compare com `gabarito/caso-N/` e confira as páginas decisivas nos PDFs. Em (c) e (d) a leitura é de juízo: o
   gabarito é conservador, e você pode discordar com a fonte na mão.

Para o relatório em Word o agente usa a biblioteca `python-docx`. Se o seu computador recusar a instalação, peça ao
agente que crie um ambiente virtual (`python3 -m venv .venv`) e instale nele.

O relatório organiza a leitura. A conferência da fonte e a decisão sobre a defesa são suas.
