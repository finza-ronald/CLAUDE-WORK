# apply-external-skills

Script para sincronizar **skills externas** (skills de terceiros, colegas, outros repositórios) com uma pasta-alvo. Mesma lógica do [apply-skills](../apply-skills/README.md), só que a origem é parametrizada e fica sempre sob `./external-skills/`.

Útil pra ter conjuntos separados de skills externas, como:

```
external-skills/
├── meu-colega-skills/
│   ├── skill-a/
│   └── skill-b/
├── outro-time-skills/
│   └── ...
```

## O que o script faz

1. **Backup primeiro, sempre.** Copia tudo de `<target-folder>/*` para `./backup-skills/<YYYY-MM-DD_HH-MM-SS>/`.
2. **Compara** os nomes de pastas em `./external-skills/<source>/` e em `<target-folder>/`.
3. **Para cada pasta presente nos dois lados**, pergunta:
   - `[s]ubstituir` — apaga a pasta no alvo e copia a da origem
   - `[i]gnorar` — deixa intacta
4. **Para cada pasta presente só na origem**, pergunta:
   - `[s]im` — copia pro alvo
   - `[n]ão` — não insere
5. Pastas que existem **só no alvo** ficam intocadas — só entram no backup.

## Como rodar

Ambas as flags `--source-folder` / `-s` e `--target-folder` / `-t` são **obrigatórias**.

A `--source-folder` **deve iniciar literalmente com `external-skills/`** (relativo à raiz do repositório). Isso deixa o caminho explícito no comando e evita erros de "esqueci de qual pasta tirar".

### Aplicar skills de um colega nas skills do Claude

```bash
python3 meta-scripts/apply-external-skills/apply_external_skills.py \
    -s external-skills/meu-colega-skills \
    -t ~/.claude/skills
```

Isso lê as skills de `./external-skills/meu-colega-skills/` e sincroniza com `~/.claude/skills/`.

### Teste seguro — sandbox

```bash
python3 meta-scripts/apply-external-skills/apply_external_skills.py \
    -s external-skills/finza-workspace/skills \
    -t .example-script-skills
```

### Modo automático

```bash
python3 meta-scripts/apply-external-skills/apply_external_skills.py \
    -s external-skills/finza-workspace/skills \
    -t ~/.claude/skills \
    --yes
```

## Flags

| Flag | Obrigatório | Descrição |
|------|-------------|-----------|
| `-s`, `--source-folder` | sim | Caminho da pasta com as skills a aplicar. **Deve iniciar com `external-skills/`**. Ex.: `external-skills/finza-workspace/skills`. |
| `-t`, `--target-folder` | sim | Pasta-alvo. Absoluto (`~/.claude/skills`) ou relativo à raiz do repositório (`.example-script-skills`). |
| `-y`, `--yes` | não | Aplica tudo sem perguntar. |
| `-h`, `--help` | não | Mostra a ajuda. |

## Erros comuns

- **`[erro] Pasta ./external-skills/ não encontrada em ...`** — crie o diretório `./external-skills/` na raiz do repositório antes de rodar.
- **`[erro] --source-folder deve iniciar com 'external-skills/' ...`** — você passou só o nome da subpasta. Inclua o prefixo: `-s external-skills/<sua-pasta>`.
- **`[erro] Pasta de origem não encontrada: ...`** — o caminho passado em `--source-folder` não existe. Confira.
- **`[erro] --source-folder deve ficar sob ./external-skills/ ...`** — o caminho usa `..` ou escapa de `./external-skills/`. Não permitido.

## Onde fica o backup

Sempre em `./backup-skills/<YYYY-MM-DD_HH-MM-SS>/`, relativo à raiz do repositório, independentemente da pasta-alvo escolhida.

## Resumo de fim de execução

```
[fim] substituídas: N | inseridas: M | ignoradas: K
```
