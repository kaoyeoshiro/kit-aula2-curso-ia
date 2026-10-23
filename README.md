# Kit da Aula 2: do chat à pasta

Caso fictício e escritório fictício (Dias & Moura). Nenhum dado é real.

## O que tem aqui

- `caso/`: contrato, aditivo e notificação (PDF).
- `escritorio/`: padrão de documentos, logo e `modelo.docx` já no padrão.
- `gabarito/`: a cronologia pronta, o Word final e a skill pronta. Só abra depois de tentar a sua.

## Como usar na aula

1. Baixe o kit (botão verde Code > Download ZIP) e abra a pasta `kit` no Claude, no ChatGPT Work ou no Codex.
2. Prática 1: peça a cronologia do caso, com os seis elementos do pedido e a regra "se não souber, diga".
   Salve como `cronologia.md` na pasta (copie o seu para a raiz do kit).
3. Prática 2: peça ao agente que crie uma skill chamada `parecer-no-padrao`. Ela lê o `cronologia.md`, preenche o
   `escritorio/modelo.docx` e salva o `cronologia.docx`. Rode a skill e confira o Word.
4. Travou? Compare com `gabarito/skills/parecer-no-padrao`, copie para a pasta de skills da sua ferramenta e rode.

O `modelo.docx` é preenchido por um script curto (`preencher.py`). Se o seu app gerar o Word direto, tudo bem:
o importante é o resultado seguir `escritorio/padrao-do-escritorio.md`.
