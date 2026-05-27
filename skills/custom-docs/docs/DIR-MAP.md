# REFERENCE_TASK_DOCS — Mapa das pastas

Convenção local de documentação do repositório de trabalho. Todas as pastas ficam em `REFERENCE_TASK_DOCS/` na raiz do repositório atual. Normalmente o usuário já adiciona essa pasta ao `.gitignore`, então pode criar arquivos sem se preocupar com poluir o repositório.

Formato padrão: `.md`. Exceções explicitadas abaixo.

---

## `PLANS/`

**Para quê:** planos de implementação gerados (e subplanos).

- Um arquivo por plano simples: `PLANS/FIN-99999.md`
- Múltiplos planos para a mesma task: subpasta `PLANS/FIN-99999/` com vários `.md` dentro (ex.: `parte-1-backend.md`, `parte-2-frontend.md`)
- Sempre usar o prefixo da task no nome (FIN-xxxxx, etc.)

**Quem escreve:** o agente (e o usuário, eventualmente).

---

## `STUDIES/`

**Para quê:** estudos de código — documentação sobre **como o repositório é hoje**.

Exemplos:
- Responsabilidades de uma classe
- Fluxo de um módulo
- Regras de negócio refletidas no código
- Levantamento de endpoints existentes para uma feature

**O que NÃO vai aqui:** planos, reports de implementação, "o que foi feito". Studies descreve o **objeto** (o repositório), não a mudança.

**Proteção:** carrega conhecimento. Antes de escrever, verifique se já existe arquivo sobre o mesmo tema e prefira atualizar.

---

## `REPORTS/`

**Para quê:** registro do **que foi feito** após uma task, alteração ou decisão.

Inclui:
- "O que foi feito" / "o que foi alterado" após a task
- Mudanças de negócio aplicadas
- Registros de decisão tomadas durante a implementação

Use prefixo da task. Múltiplos reports da mesma task → subpasta `REPORTS/FIN-99999/`.

**Quem escreve:** o agente (e o usuário).

---

## `PROMPTS/` *(protegida)*

**Para quê:** prompts escritos pelo usuário — para implementações, geração de planos, correções.

**Regra:** o agente **não edita** esta pasta a menos que o usuário peça explicitamente. Pode ler para contexto.

---

## `TEMP/`

**Para quê:** rascunho, dump, descartável.

- JSON exportado, `.md` que não cabe em nenhuma outra pasta, cópia de arquivo, report sem valor de longo prazo, anotação temporária.
- Aceita qualquer formato (não precisa ser `.md`).
- Quando estiver em dúvida sobre onde salvar algo, **prefira `TEMP/`** em vez de inventar pasta.

---

## `CODE-MAPPER/`

**Para quê:** mapeamentos diretos do código — "qual parte faz o quê, em qual módulo, em qual arquivo".

- Relacionado a `STUDIES/`, mas mais seco e direto: cada seção do `.md` é um mapeamento simples (ex.: feature X → arquivo Y → função Z).
- Provavelmente não será relido inteiro, mas agrega conhecimento útil durante uma implementação.

**Quem escreve:** quase sempre o agente.

---

## `BUSINESS-RULES/` *(protegida)*

**Para quê:** regras de negócio — o que **não é código**, mas o conhecimento de negócio por trás dele.

Uma regra de negócio pode estar implementada no código, mas sua **origem** está fora do código (decisão do produto, contrato, regulação).

**Regra:** o agente **não edita** esta pasta a menos que o usuário peça explicitamente. Pode (e deve) ler para entender contexto.

---

## `INTEGRATION-NOTES/`

**Para quê:** trazer conhecimento de **outros sistemas/repositórios** para dentro do repositório atual.

Exemplos:
- Trabalhando no frontend, anotações sobre o backend ficam aqui
- Trabalhando no backend, anotações sobre o frontend ficam aqui
- Doc de um sistema externo (do usuário ou de terceiro) relevante para a integração

Aceita formatos além de `.md` quando fizer sentido (ex.: schema JSON, exemplo de payload).

---

## `DECISIONS/`

**Para quê:** decisões **agnósticas a um trecho específico de código** — diretrizes que orientam tasks futuras ou o agente.

Diferença de `REPORTS/`: report é "o que foi feito"; decision é "como decidimos que faremos daqui em diante".

---

## Resumo rápido

| Pasta | Quem escreve | Foco |
|---|---|---|
| `PLANS/` | agente + usuário | o que vai ser feito |
| `STUDIES/` | agente + usuário | como o código é hoje (analítico) |
| `REPORTS/` | agente + usuário | o que foi feito |
| `PROMPTS/` | **só usuário** | prompts do usuário |
| `TEMP/` | qualquer | descartável / sem categoria |
| `CODE-MAPPER/` | agente | mapa direto código→responsabilidade |
| `BUSINESS-RULES/` | **só usuário** | regra de negócio (externa ao código) |
| `INTEGRATION-NOTES/` | agente + usuário | conhecimento de outros sistemas |
| `DECISIONS/` | agente + usuário | diretrizes para tasks futuras |
