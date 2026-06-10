---
name: custom-docs
description: Convenção de documentação local do repositório em uma pasta `REFERENCE_TASK_DOCS/`. Use quando precisar criar, ler ou salvar planos de implementação, estudos de código, reports do que foi feito, mapeamentos de código, regras de negócio, notas de integração, decisões, prompts do usuário ou arquivos temporários. Sempre que for gerar um plano, study, report, code-map, integration-note ou rascunho temporário, esta skill define onde o arquivo deve ser salvo.
---

# custom-docs

Esta skill descreve a convenção de documentação local usada **no repositório de trabalho atual** (não global, não nesta máquina — sempre relativo ao repositório aberto).

A convenção é simples: cada repositório tem (ou pode ter) uma pasta `REFERENCE_TASK_DOCS/` na raiz, com subpastas fixas para cada tipo de artefato de documentação. Quase todos os arquivos são `.md`.

> Essas pastas normalmente estão no `.gitignore` (o usuário cuida disso). **Não se preocupe em "sujar" o repositório** ao criar arquivos aqui — esse é o propósito.

## Quando usar

Sempre que você for **criar** ou **procurar** um destes artefatos no repositório atual:

- Plano de implementação ou subplano → `PLANS/`
- Estudo de código / fluxo / módulo / endpoint → `STUDIES/`
- "O que foi feito" após uma task / decisão de implementação / changelog interno → `REPORTS/`
- Mudanças feitas no código, como refatorações, deleções, novo código implementado, tudo mapeado de forma simples e direta, em seções organizadas -> `CHANGES/`
- Mapeamento do trabalho executado, para posterior consulta, sobre o que foi feito, em quanto tempo, para que -> `WORK/`
- Mapeamento direto de onde-está-o-quê no código → `CODE-MAPPER/`
- Regra de negócio (informação externa ao código) → `BUSINESS-RULES/` *(não editar sem pedido explícito)*
- Documento de outro sistema/repositório trazido como referência (ex.: doc do backend enquanto se trabalha no frontend) → `INTEGRATION-NOTES/`
- Decisão técnica/agnóstica que orienta tasks futuras → `DECISIONS/`
- Prompt escrito pelo usuário → `PROMPTS/` *(não editar sem pedido explícito)*
- Rascunho, dump, cópia, JSON exportado, report descartável → `TEMP/`

Se um artefato não se encaixa em nenhuma das pastas acima, **prefira `TEMP/`** em vez de inventar pasta nova.

## Como usar

1. Antes de criar o arquivo, confira se `REFERENCE_TASK_DOCS/` existe na raiz do repositório atual. Se não existir, crie a pasta e a subpasta necessária.
2. Salve o arquivo `.md` na subpasta correta seguindo a convenção em [docs/DIR-MAP.md](docs/DIR-MAP.md).
3. Para `PLANS/` e `REPORTS/`, **use o prefixo da task** (ex.: `FIN-99999`) no nome do arquivo. Se uma task tem múltiplos planos/reports, agrupe em uma subpasta `PLANS/FIN-99999/` ou `REPORTS/FIN-99999/`.
4. Para `TEMP/` e `INTEGRATION-NOTES/`, outros formatos além de `.md` são aceitos (json, txt, cópias de arquivos).
5. Para `CHANGES/`, siga uma estrutura com o prefixo da task no nome (ex.: `FIN-99999-changes.md`). Apenas um arquivo por task.

## Pastas protegidas

Não edite arquivos em `PROMPTS/` e `BUSINESS-RULES/` a menos que o usuário peça explicitamente. Estas pastas são de curadoria humana.

`STUDIES/` e `BUSINESS-RULES/` carregam conhecimento valioso — leia antes de escrever sobre o mesmo tema, e prefira atualizar a criar duplicata.

## Detalhes de cada pasta

Consulte [docs/DIR-MAP.md](docs/DIR-MAP.md) para a descrição completa de cada subpasta, o que vai (e o que não vai) dentro dela, e as regras de nomeação.
