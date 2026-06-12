# Procedimento técnico — Relatório de subtarefas e tempo registrado no Jira

Procedimento read-only para coletar a partir de cards-pai do Jira (Stories/Tasks) a lista de subtarefas, histórico de mudanças, e worklogs (registro de atividades / tempo registrado), e então montar uma tabela resumo.

Toda a operação é **read-only**: não usar tools de escrita do Atlassian (`editJiraIssue`, `addWorklogToJiraIssue`, `transitionJiraIssue`, `addCommentToJiraIssue`, etc.).

---

## 1. Pré-requisitos

### Tools MCP necessárias

Carregar via `ToolSearch` antes do uso (são deferred):

```
ToolSearch select:mcp__claude_ai_Atlassian__getAccessibleAtlassianResources,mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql,mcp__claude_ai_Atlassian__getJiraIssue
```

### Descobrir `cloudId`

A primeira chamada de qualquer fluxo deve ser:

```
mcp__claude_ai_Atlassian__getAccessibleAtlassianResources()
```

Retorna lista de sites Atlassian acessíveis. Pegar o `id` (UUID) do site relevante (no projeto Finza é `blips-dev.atlassian.net`). O `cloudId` se mantém estável; pode ser cacheado entre chamadas da mesma sessão.

Para o site Finza atual:
- `cloudId` = `bdf1e95c-e983-4f89-b951-75929e17bb54`
- `baseUrl` = `https://blips-dev.atlassian.net`

---

## 2. Coletar subtarefas dos cards-pai

Use `searchJiraIssuesUsingJql` com query `parent in (...)`:

```jsonc
{
  "cloudId": "<cloudId>",
  "jql": "parent in (FIN-1100, FIN-1079, FIN-1027, FIN-796)",
  "fields": ["summary", "status", "issuetype", "parent"],
  "maxResults": 100
}
```

### Cuidado com tamanho do payload

A resposta inclui muito metadado (avatars, project info) — pode estourar o limite do contexto.

Se o tool retornar `Error: result exceeds maximum allowed tokens. Output has been saved to <file>`, use `jq` para extrair só o necessário:

```bash
jq '.issues.nodes | map({key, parent: .fields.parent.key, summary: .fields.summary, status: .fields.status.name, type: .fields.issuetype.name})' <arquivo-salvo>
```

### Filtros úteis no JQL

- `parent = FIN-X` — subtarefas de um único pai
- `parent in (FIN-A, FIN-B, FIN-C)` — multi-pai
- `assignee = currentUser()` — só do usuário atual
- `status != Cancelled` — excluir canceladas

---

## 3. Coletar histórico (changelog) por subtarefa

`getJiraIssue` com `expand=changelog`:

```jsonc
{
  "cloudId": "<cloudId>",
  "issueIdOrKey": "FIN-XXXX",
  "expand": "changelog",
  "fields": ["summary"]
}
```

O changelog vem em `.issues.nodes[0].changelog.histories[]`. Cada `history`:

```jsonc
{
  "created": "2026-05-26T14:17:48.454-0400",
  "author": { "displayName": "Ronald Seabra", ... },
  "items": [
    { "field": "status", "fromString": "Doing", "toString": "Done" }
  ]
}
```

### Filtros recomendados ao processar

- **Ignorar items** cujo `field` seja `timespent`, `timeestimate` ou `WorklogId` — são ruído de worklog que polui o histórico. (Para tempo registrado use o passo 4 com `fields=["worklog"]`.)
- **Manter**: `status`, `assignee`, `summary`, `description`, `IssueParentAssociation`, `priority`, `labels`, `customfield_*`.
- Se um `history` só contém items ignorados, descartar inteiro.
- Para `field: description`, NÃO copiar o conteúdo todo — substituir por `(definido)` ou `(editado)` baseado se `fromString` era null.

### Paralelismo

Sempre buscar **5-7 changelogs em paralelo** (um único message com múltiplas tool calls). Cada chamada retorna ~7-10KB. Se for >20 subtarefas, considerar usar Agent (subagent) para não inflar o contexto principal.

### Performance esperada

- 1 subtask = ~1s, ~10KB output
- 30 subtasks = ~30s em batches de 6, ~300KB total
- Acima disso → delegar a um subagente que retorne só o markdown formatado

---

## 4. Coletar worklog (registro de atividades / tempo registrado)

`getJiraIssue` com `fields=["worklog"]` (sem `expand=changelog`):

```jsonc
{
  "cloudId": "<cloudId>",
  "issueIdOrKey": "FIN-XXXX",
  "fields": ["worklog"]
}
```

Worklogs vêm em `.issues.nodes[0].fields.worklog.worklogs[]`. Cada entry:

```jsonc
{
  "author": { "displayName": "Ronald Seabra" },
  "started": "2026-05-26T08:30:00.000-0400",
  "timeSpent": "2h 30m",          // string legível
  "timeSpentSeconds": 9000,       // numérico
  "comment": { /* ADF — ver abaixo */ },
  "id": "55813"
}
```

### Parsing do campo `comment` (ADF)

Comments vêm em [Atlassian Document Format](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/) — JSON aninhado tipo:

```jsonc
{
  "type": "doc",
  "content": [
    { "type": "paragraph", "content": [{ "type": "text", "text": "..." }] },
    { "type": "bulletList", "content": [
      { "type": "listItem", "content": [
        { "type": "paragraph", "content": [{ "type": "text", "text": "..." }] }
      ]}
    ]}
  ]
}
```

Para extrair texto, walk recursivo coletando `text` em qualquer nível:

```python
import json, sys
def extract(node, lines):
    if isinstance(node, dict):
        if node.get("type") == "text":
            lines.append(node.get("text", ""))
        for v in node.values():
            extract(v, lines)
    elif isinstance(node, list):
        for v in node:
            extract(v, lines)

data = json.load(sys.stdin)
lines = []
extract(data, lines)
print(" | ".join(l for l in lines if l.strip()))
```

Use ` | ` como separador para juntar bullets/parágrafos em uma linha.

### `jq` alternativo

```bash
jq '.issues.nodes[0] | {
  key,
  summary: .fields.summary,
  worklogs: .fields.worklog.worklogs | map({
    started,
    author: .author.displayName,
    timeSpent,
    timeSpentSeconds,
    comment_text: [.. | objects | select(.type == "text") | .text] | join(" | ")
  })
}' <arquivo-salvo>
```

---

## 5. Filtrar worklogs por data (modo "tempo de hoje")

Use JQL com `worklogDate` + `worklogAuthor`:

```jsonc
{
  "jql": "worklogDate = \"2026-05-26\" AND worklogAuthor = currentUser()",
  "fields": ["summary", "parent"]
}
```

Isso retorna **apenas issues** que tiveram worklog na data informada. Aí para cada issue retornada, chame `getJiraIssue` com `fields=["worklog"]` e filtre os worklogs cujo `started` cai no dia desejado (uma issue pode ter worklogs de várias datas; o JQL só identifica a issue, não o worklog específico).

### Filtro de data por timezone

`worklogDate` no JQL é interpretado no fuso do servidor Atlassian. Os campos `started` retornados vêm com offset (`-0400`, etc.). Para "hoje em São Paulo", filtrar `started` cuja porção de data (após ajuste UTC-3) bate com a data atual.

Para "esta semana": `worklogDate >= startOfWeek() AND worklogDate <= endOfWeek()`.
Para "mês corrente": `worklogDate >= startOfMonth()`.

---

## 6. Montagem da tabela final

### Conversão de tempo

`timeSpentSeconds` → string formatada:

```python
def fmt(secs):
    h, m = divmod(secs // 60, 60)
    return f"{h}h {m:02d}m"
```

### Tabela por subtarefa (verbose)

```markdown
### FIN-XXXX — <summary>
- <YYYY-MM-DD HH:MM> (UTC-X) — <autor> — registrou **<timeSpent>**
  - <comment_text resumido>

**Total: Xh Ym**
```

### Tabela resumo por card pai (compacto)

```markdown
| Card pai | Subtarefa | Resumo | Horário | Tempo |
|----------|-----------|--------|---------|-------|
| FIN-1100 | [FIN-1132](url) | ... | 09:30 | **2h 30m** |
...

| Card pai | Subtarefas (hoje) | Total |
|----------|-------------------|-------|
| FIN-1100 — Aprovar e reprovar... | 2 | **4h 00m** |
...
| **Total geral** | **N entries** | **Xh Ym** |
```

### Convenções de timezone

- Timestamps do Jira vêm em UTC com offset (geralmente `-0400`)
- Para horário "local" São Paulo, somar +1h ao valor com `-0400`
- Sempre marcar explicitamente o fuso na saída final (ex: "Horários em fuso São Paulo / UTC-3")

---

## 7. Onde salvar o relatório final

Sempre em `REFERENCE_TASK_DOCS/TEMP/<YYYY-MM-DD>-<HHMM>-subtarefas.md`:

```bash
date "+%Y-%m-%d-%H%M"   # ex: 2026-05-26-1801
```

Arquivo final: `REFERENCE_TASK_DOCS/TEMP/2026-05-26-1801-subtarefas.md`

Estrutura padrão do arquivo:

```markdown
# Subtarefas — <descrição do escopo> — <data>

Gerado em: <YYYY-MM-DD HH:MM> (BRT)
Cards-pai consultados: FIN-X, FIN-Y, ...

## <Seção 1: lista de subtarefas, se pedido>
...

## <Seção 2: histórico, se pedido>
...

## <Seção 3: worklogs, se pedido>
...

## <Seção 4: tabelas-resumo>
| ... |
```

---

## 8. Resumo decisório (quando usar o quê)

| Pedido do usuário | Tool/campo a usar |
|---|---|
| "listar subtarefas dos cards X, Y" | `searchJiraIssuesUsingJql` com `jql=parent in (X, Y)` |
| "histórico/atividade/mudanças de status" | `getJiraIssue` com `expand=changelog` |
| "tempo registrado / registro de atividades / worklog / horas" | `getJiraIssue` com `fields=["worklog"]` |
| "o que registrei hoje/esta semana/este mês" | JQL `worklogDate = ...` + `worklogAuthor = currentUser()` → depois worklog por issue |
| "tempo gasto em uma tarefa específica" | `getJiraIssue` com `fields=["worklog"]` na issue diretamente |

---

## 9. Armadilhas conhecidas

1. **`timespent` no changelog ≠ worklog completo.** O changelog mostra deltas (`timespent: 3600 → 7200` = +1h), mas não traz o comment. Para o relatório de atividades real, usar sempre `fields=["worklog"]`.
2. **`worklogDate` em JQL retorna a issue, não o worklog.** Uma issue com 5 worklogs em datas diferentes aparece uma única vez; é preciso buscar os worklogs e filtrar por `started` no agente.
3. **Tool `mcp__claude_ai_Atlassian__fetch` aceita só ARI.** Não dá pra chamar endpoints REST arbitrários do Jira. Para worklogs use sempre `getJiraIssue` com `fields=["worklog"]`.
4. **Output de `searchJiraIssuesUsingJql` com muitas issues estoura limite.** Se passar de ~10 issues, o tool salva em arquivo e devolve o path — usar `jq` direto no arquivo.
5. **ADF do comment pode ser profundamente aninhado** (bulletList → listItem → paragraph → text). Walk recursivo é mais robusto que jq encadeado.
6. **Status traduzido vs canônico.** O campo `name` no status pode vir em PT-BR ("Concluído") ou EN ("Done") dependendo da configuração da issue. Para filtros use o `statusCategory.key` (`new` / `indeterminate` / `done`).

---## 11. Registrar e distribuir tempo (modo escrita — opcional)

> A coleta (seções 1–10) é read-only. Este modo **escreve** worklog e só deve rodar mediante pedido explícito do usuário.

### Registrar
- Tool: `addWorklogToJiraIssue` (`timeSpent` ex. `"1h 30m"`, `started` ISO 8601 com offset ex. `2026-06-09T09:15:00.000-0300`, `commentBody` em markdown com lista técnica de 5+ itens).
- Atualizar um worklog existente: passar `worklogId` (mantém comentário, muda `started`/`timeSpent`).
- O servidor normaliza o offset (`-0300` → `-0400`); o instante e a **data** permanecem corretos.

### Pesos por score
- Pontuar cada subtarefa de **1 a 10** combinando 3 eixos: **volume** (linhas), **complexidade** (lógica nova vs. código movido/mecânico) e **risco** (toca produção / muda comportamento).
- O score vira **peso relativo** na divisão do tempo.

### Distribuir encaixando a jornada
1. Tempo útil = jornada − almoço (ex.: 9:15–18:00 − 2h = **6h45m** = 405 min).
2. Subtrair o que já está registrado; o resto é o bolo a distribuir.
3. `tempo_i = resto × peso_i / Σpesos`, arredondado a múltiplos de 5 min **mantendo a soma exata**.
4. **Encadear cronologicamente** respeitando blocos manhã/tarde e o almoço; ordem técnica coerente (ex.: testes de garantia antes do refactor; correção de testes depois do split).
5. `started` de cada worklog no slot calculado.


## 10. Exemplo completo (resumo do fluxo)

```
1. ToolSearch select:mcp__claude_ai_Atlassian__getAccessibleAtlassianResources,...
2. getAccessibleAtlassianResources() → pegar cloudId
3. searchJiraIssuesUsingJql(jql="parent in (FIN-1100, FIN-1079)") → lista subtarefas
   - Se >10 issues, ler do arquivo salvo via jq
4. Para cada subtarefa (em paralelo, batches de 5-7):
   getJiraIssue(issueIdOrKey="FIN-X", fields=["worklog"])
   - extrair worklogs.worklogs[]
   - converter timeSpentSeconds em formato legível
   - extrair texto do comment ADF via walk recursivo
5. Agregar por card pai e gerar:
   - Tabela detalhada (por worklog)
   - Tabela resumo (por card pai)
   - Total geral
6. Salvar em REFERENCE_TASK_DOCS/TEMP/<YYYY-MM-DD>-<HHMM>-subtarefas.md
```

Para volumes >25 subtarefas, delegar passos 3-5 a um subagente via `Agent` tool (subagent_type=general-purpose) com instruções explícitas sobre cloudId, fields, e formato de saída esperado.

## 11. Registrar e distribuir tempo (modo escrita — opcional)

> A coleta (seções 1–10) é read-only. Este modo **escreve** worklog e só deve rodar mediante pedido explícito do usuário.

### Registrar
- Tool: `addWorklogToJiraIssue` (`timeSpent` ex. `"1h 30m"`, `started` ISO 8601 com offset ex. `2026-06-09T09:15:00.000-0300`, `commentBody` em markdown com lista técnica de 5+ itens).
- Atualizar um worklog existente: passar `worklogId` (mantém comentário, muda `started`/`timeSpent`).
- O servidor normaliza o offset (`-0300` → `-0400`); o instante e a **data** permanecem corretos.

### Pesos por score
- Pontuar cada subtarefa de **1 a 10** combinando 3 eixos: **volume** (linhas), **complexidade** (lógica nova vs. código movido/mecânico) e **risco** (toca produção / muda comportamento).
- O score vira **peso relativo** na divisão do tempo.

### Distribuir encaixando a jornada
1. Tempo útil = jornada − almoço (ex.: 9:15–18:00 − 2h = **6h45m** = 405 min).
2. Subtrair o que já está registrado; o resto é o bolo a distribuir.
3. `tempo_i = resto × peso_i / Σpesos`, arredondado a múltiplos de 5 min **mantendo a soma exata**.
4. **Encadear cronologicamente** respeitando blocos manhã/tarde e o almoço; ordem técnica coerente (ex.: testes de garantia antes do refactor; correção de testes depois do split).
5. `started` de cada worklog no slot calculado.
