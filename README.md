# CLAUDE-WORK

Workspace de skills e scripts auxiliares para o Claude Code. As skills locais ficam em `./skills/` e as de terceiros em `./external-skills/<origem>/`. Os scripts abaixo aplicam essas skills numa pasta-alvo (geralmente `~/.claude/skills`), sempre com backup automático em `./backup-skills/<timestamp>/`.

## Scripts

### [meta-scripts/apply-skills/](meta-scripts/apply-skills/)

Sincroniza as skills locais (`./skills/`) com uma pasta-alvo. Pergunta uma a uma se quer substituir as existentes e inserir as novas. Detalhes em [meta-scripts/apply-skills/README.md](meta-scripts/apply-skills/README.md).

```bash
python3 meta-scripts/apply-skills/apply_skills.py -t ~/.claude/skills
```

### [meta-scripts/apply-external-skills/](meta-scripts/apply-external-skills/)

Mesma lógica do `apply-skills`, mas a origem fica sob `./external-skills/<colega-ou-time>/`. Útil pra aplicar skills de terceiros sem misturar com as suas. Detalhes em [meta-scripts/apply-external-skills/README.md](meta-scripts/apply-external-skills/README.md).

```bash
python3 meta-scripts/apply-external-skills/apply_external_skills.py \
    -s external-skills/finza-workspace/skills -t ~/.claude/skills
```

## Pastas

- **`skills/`** — skills locais (origem padrão do `apply-skills`).
- **`external-skills/`** — skills externas organizadas por origem (`<colega>/skills/`).
- **`backup-skills/`** — backups automáticos da pasta-alvo (gitignored).
- **`.example-script-skills/`** — sandbox para testar os scripts com segurança (gitignored).
