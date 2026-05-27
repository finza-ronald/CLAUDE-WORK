# CodeGraphContext MCP

Ferramenta para análise de código em grafo. Permite explorar relações, dependências, fluxos e conhecimento estruturado do repositório.

## Casos de uso

| Necessidade | Comando | Descrição |
|---|---|---|
| Quem chama esta função? | `find_callers` | Lista todas as funções que chamam a função específica |
| O que esta função chama? | `find_callees` | Lista todas as funções que a função chama |
| Rastrear fluxo completo | `call_chain` | Mostra a cadeia de chamadas de uma função até o fim |
| Entender hierarquia de classes | `class_hierarchy` | Mostra herança e relações entre classes |
| Encontrar importadores | `find_importers` | Lista quais arquivos/módulos importam um módulo específico |
| Detectar código morto | `dead_code` | Encontra funções que nunca são chamadas |
| Calcular complexidade | `calculate_cyclomatic_complexity` | Mede a complexidade de uma função |
| Dependências entre módulos | `module_deps` | Mostra relações de dependência entre módulos |
| Quem modifica uma variável? | `who_modifies` | Encontra onde uma variável é alterada |
| Procurar por padrão | `find_code` | Busca funções, classes ou conteúdo por keyword |

## Antes de usar

1. **Verifique se o repositório está indexado:**
   ```
   list_indexed_repositories
   ```
   Se não estiver, adicione:
   ```
   watch_directory (para live updates) ou add_code_to_graph (scan único)
   ```

2. **Para melhor performance:** use `repo_path` para restringir a busca ao repositório atual.

## Exemplo de fluxo

```
1. Usuário diz: "quem chama getUserData?"
2. Você usa: find_callers(target: "getUserData", repo_path: "/projeto/atual")
3. Resultado mostra todas as funções que chamam getUserData
4. Se precisar ver o fluxo completo, use: call_chain(target: "getUserData")
```

## Dicas

- Use `find_code` quando não souber exatamente o nome da função
- Para refatoração grande, comece com `dead_code` para ver o que pode ser removido
- Use `class_hierarchy` antes de alterar classes base
- `module_deps` ajuda a entender acoplamento e identificar módulos para desacoplar
