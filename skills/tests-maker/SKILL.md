---
name: tests-maker
description: Skill para criação, refatoração e correção de testes com pytest. Use quando precisar criar testes unitários, extrair testes de uma feature ou task implementada, corrigir testes após mudança no código, ou aplicar boas práticas em testes existentes. Fornece indicadores de boas práticas, exemplos e checklist sobre estrutura, fixtures, mocks, asserts, model_bakery e nomenclaturas.
---

# tests-maker

Skill para criação de testes com pytest no repositório de trabalho atual. Define boas práticas, convenções e checklist a serem seguidos ao escrever testes, refatorar testes existentes ou ajustar testes após mudanças no código.

## Quando usar

- Criar testes unitários/funcionais para uma feature, task ou código alterado.
- Extrair testes a partir de uma implementação recém-feita.
- Corrigir/atualizar testes existentes após mudança no código.
- Refatorar testes para aplicar boas práticas (asserts progressivos, fixtures, mocks com `spec=`, etc.).
- Revisar um arquivo de teste para sugerir melhorias.

## Ferramentas e bibliotecas

- **pytest** como runner.
- **model_bakery** para inserção de dados no banco.
- Recursos do framework em uso (Django, FastAPI, Flask, etc.) — preferir o que já vem da lib em vez de reescrever.
- Conferir `pyproject.toml` para libs disponíveis antes de criar utilitário próprio.

## Estrutura e localização

- Testes vão na pasta `tests/` de cada app.
- Sempre procurar o arquivo de teste **existente** mais aderente ao assunto antes de criar um novo.
- Antes de nomear um teste, verifique nomenclaturas usadas em testes próximos para manter consistência.

## Formato dos testes

- Testes são **funcionais** (funções `def test_...`), **não classes**.
- Maioria são testes funcionais (integração leve), evitando mocks genéricos.

## Princípios resumidos

Detalhes e exemplos em [docs/BEST-PRACTICES.md](docs/BEST-PRACTICES.md). Resumo:

- **Fixtures**: procurar em `conftest.py` antes de criar; reaproveitar fixtures/factories alterando o retorno dentro do teste (com comentário do "por quê").
- **Docstrings**: docstring curta em cada teste; docstring no topo do arquivo descrevendo o que e quais cenários são cobertos.
- **Arrange / Action / Assert**: mínimo de dados no arrange; comentário no action quando não óbvio; asserts progressivos no assert.
- **Asserts de API**: usar variáveis `expected_*` com nomes descritivos.
- **Mocks**: usar `spec=` apontando para a classe origem sempre que possível.
- **Comentários**: apenas quando agregam (expectativa não óbvia, regra de negócio sobre dado, importância de um dado inserido no banco). Nada óbvio.
- **Dados no banco**: preferir `model_bakery`; comentar dados importantes que não são salvos em variável.
- **Helpers**: evitar funções auxiliares e funções "cria dado no banco" — manter a manipulação dentro do próprio teste.
- **Timezone (Django)**: salvar com timezone para evitar warnings.
- **Não sobrescrever** classes/funções existentes dentro do teste — usar gerenciadores de contexto e mocks adequados.

## Anti-padrões a evitar

- Comentários óbvios sobre `if`s descritivos, funções e variáveis com nomes claros.
- `getattr`/`hasattr` para "ver se a propriedade existe".
- Variáveis declaradas e não usadas.
- Recriar fixtures/factories já existentes apenas porque um dado é diferente.
- Criar funções auxiliares "só para inserir dado no banco".
- Mocks genéricos sem `spec=`.

## Sugestões adicionais

Ao terminar um teste, **sugerir outros cenários** ao usuário (caminho infeliz, edge cases, validações, permissões, integrações afetadas).

## Detalhes completos

Convenção completa, com exemplos e justificativas para cada regra, em [docs/BEST-PRACTICES.md](docs/BEST-PRACTICES.md).
