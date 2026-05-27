---
name: code-suggest
description: Sugestões e ferramentas para análise de código. Use quando precisar explorar relações no código, dependências, fluxos, e conhecimento em grafo. Define quais MCPs e comandos usar para cada tipo de análise.
---

# code-suggest

Esta skill reúne as melhores práticas e ferramentas para análise de código no repositório de trabalho atual.

## MCPs disponíveis

### CodeGraphContext

**Para quê:** procurar relações, dependências e conhecimento em grafo do código.

Use quando precisar:
- Encontrar quem chama uma função (`find_callers`)
- Ver o que uma função chama (`find_callees`)
- Rastrear importações e módulos (`find_importers`)
- Entender fluxos de chamadas (`call_chain`)
- Detectar código morto (`dead_code`)
- Analisar hierarquia de classes (`class_hierarchy`)
- Calcular complexidade ciclomática
- Mapeamento de dependências entre módulos

Documentação e detalhes de uso estão em [docs/CODEGRAPH.md](docs/CODEGRAPH.md).
