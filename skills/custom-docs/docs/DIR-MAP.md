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

## `CHANGES/`

**Para quê:** registro de alterações feitas no código, de forma direta e simples.

**Template:**
* Usar seções e subseções, dar preferencia à seções e subseções ao invés de gráficos.
* As seções pais, são sempre as grandes etapas do que foi feito. Exemplo, se no primeiro dia eu criei todo um módulo, essa é uma seção. Se no segundo do dia eu fiz algo não associado à isso, como a criação de outro módulo de funcionalidades diferentes, essa é outra seção. Mas de preferência, considerar que é tudo um mesmo escopo.
* As primeiras subseções (pra cada seção), são: "Deleções", "Refatoração", "Novas implementações", "Correções", "Testes", "Alterações de funcionamento", "Novas implementações sem impacto de fluxo", "Documentação"
* As próximas subseções, são livres pra cada escopo. Mas deve ter uma subseção obrigatória: "Impacto", que é uma subseção de no máximo 4 linhas. Simples, direta, e TÉCNICA.
* Evite gráficos e diagramas, e tabelas, e esquemas complexos. Dê preferencia ao uso de estruturas unidimensionais: Seções, Subseções, Listas.
* Aproveite de recursos visuais "inline" e "textuais"
* Aproveite de termos técnicos que condensem as mudanças

**Regra**:
* Sem registrar regras de negócios.
* Sem registrar motivações, ou impactos de negócio. Apenas registros de impacto técnico entre códigos. Apenas um arquivo por task.
* Descrição direta e simples da mudança. Sem exemplo de código, apenas a referência das linhas, nome dos métodos/funções e classes, path relativo do arquivo, e descrição de no máximo (MÁXIMO) três linhas

---

## `RECIPES/`

**Para quê:** Recipes são manuais e instruções para o agente fazer alguma operação dentro do código ou para o agente implementar algo.
São arquivos .md, criados pelo agente ou pelo usuário, que descrevem os passos e verificações para realizar algum implementação no código, como um novo status em um entidade,
ou descrevem um formato ação, como por exemplo como fazer scrapper de uma página web.

**Template:**
* Arquivos didáticos, detalhados e com exemplos.
* Explicação clara de casos de uso, e das condições das instruções
* Usos de fluxogramas, tabelas, e recursos visuais que ajudem a visualizar o fluxo para a mudança.
* Apoio dos recursos visuais com recursos linguísticos, ou seja, resumo em texto de cada coisa.
* Descrição dos objetivos da recipe, seguidos dos casos de uso e dos casos de não uso
* Indicação do resultado esperado de cada passo, e de como revisar cada passo, se for preciso
* Nomes de arquivos longos e descritivos

## `WORK/`

**Para quê:** Em work, registramos um arquivo .md para um tarefa feita, registrando o trabalho que fizemos. Isso pode ser solicitado ao agent, ou escrito direto pelo usuário. Essa é uma forma de rastrearmos a complexidade e a motivação de tudo que foi feito durante o trabalho.

**Template:**
* Uma sub-pasta pra cada dia. Exemplo: ....WORK/12-06-2026/FIN-1251.md
* Arquivos .md únicos pra cada task. Exemplo, FIN-1251.md
* Cada novo registro (escopo do que foi feito), deve ser uma nova seção ou subseção
* A maior seção pai do arquivo é sempre a data e o horário do trabalho
* A subseções são sempre os escopos dos trabalhos realizados
* As subseções devem ter: horário solicitado de registro (que horas foi adicionado ao arquivo), horário de início do trabalho daquele escopo, duração estimada do trabalho realizado
* A descrição do trabalho deve conter infos dos arquivos alterados, volume do trabalho, complexidade, risco das alterações e impactos
* Usar bastante listas para descrever cada trabalho
* Separar visualmente dias diferentes, ou escopos de trabalhos diferentes com "---" (markdown)
* Seções de dia de trabalho, devem ter a informação do nome da branch trabalhada, se disponível

**Regras:** Caso o nome da task nao seja fornecido, pode se basear no nome da branch (procure pelo prefixo FIN-NUMBER). Apenas um arquivo por task


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
| `CHANGES/` | agente | mapeamento de mudanças técnicas de código |
| `RECIPES/` | agente + usuário | instruções para implementações ou ações |
| `WORK/` | agente | registro de trabalho realizado, com infos de volume, complexidade, e duração |
