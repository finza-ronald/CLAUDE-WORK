---
name: work-track
description: Análise de trabalho registrado no Jira. Use quando o usuário pedir explicitamente relatórios sobre seu trabalho — como "registro do trabalho de hoje", "tabela do trabalho", "horas trabalhadas", "tempo registrado", "o que fiz", "atividades do dia", etc. Coleta subtarefas, histórico de mudanças e worklogs (tempo registrado), e monta relatório detalhado por subtarefa em REFERENCE_TASK_DOCS/TEMP/.
---

# work-track

Skill para gerar relatórios de trabalho registrado no Jira, baseado em análise read-only de subtarefas, histórico e worklogs.

## Quando usar

Sempre que o usuário pedir **explicitamente** um relatório sobre seu trabalho:

- "registro do trabalho de hoje"
- "tabela do trabalho de hoje"
- "horas trabalhadas em X"
- "tempo registrado nas tarefas"
- "o que fiz hoje"
- "atividades do dia"
- "resumo de worklogs"
- Qualquer outra frase que indique **análise de trabalho registrado**

## O que retorna

Um relatório markdown salvo em `REFERENCE_TASK_DOCS/TEMP/` com:

- **Detalhes por subtarefa**: cada subtarefa com seus worklogs, horários, tempo registrado e comentários
- **Tabelas-resumo**: agregação por card-pai, totais por dia
- **Histórico (opcional)**: mudanças de status e edições se solicitado

## Procedimento completo

Veja [docs/PROCEDIMENTO.md](docs/PROCEDIMENTO.md) para o fluxo técnico passo-a-passo:
- Como descobrir o `cloudId`
- Coletar subtarefas, histórico e worklogs
- Filtros por data/autor/card
- Parsing de ADF (comments)
- Paralelismo e performance
- Armadilhas conhecidas
