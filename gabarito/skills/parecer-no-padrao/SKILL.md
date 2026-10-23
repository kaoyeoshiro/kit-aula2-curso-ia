---
name: parecer-no-padrao
description: Gera o cronologia.docx no padrão do escritório Dias & Moura a partir do cronologia.md da pasta. Use quando o usuário pedir a cronologia ou o parecer em Word no padrão do escritório.
---

# Parecer no padrão do escritório

1. Leia o `cronologia.md` e o `padrao-do-escritorio.md` da pasta do caso.
2. Rode `python3 preencher.py cronologia.md escritorio/modelo.docx cronologia.docx`, com o `preencher.py` desta skill.
   O script precisa de `python-docx` (`pip install python-docx`). O modelo já traz logo, cabeçalho, tabela e rodapé.
3. Confira se a tabela tem uma linha por fato, com data no formato dd/mm/aaaa, e se a seção "Pontos para conferência
   humana" lista tudo o que ficou sem fonte.
4. Salve o `cronologia.docx` na pasta e diga ao usuário o que ele precisa conferir.

Regra fixa: se um dado não está nos documentos, escreva "Não encontrei nos documentos". Nunca complete por conta própria.
