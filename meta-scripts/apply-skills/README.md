# apply-skills

Script para sincronizar as skills locais do repositório (`./skills/`) com uma pasta-alvo — geralmente `~/.claude/skills`, mas pode ser qualquer pasta (útil pra testar antes em uma pasta sandbox).

## O que o script faz

1. **Backup primeiro, sempre.** Copia tudo de `<target-folder>/*` para `./backup-skills/<YYYY-MM-DD_HH-MM-SS>/`. Mesmo se você cancelar depois, o backup já está em disco.
2. **Compara** os nomes de pastas em `./skills/` e em `<target-folder>/`.
3. **Para cada pasta presente nos dois lados** (skill já existe no alvo), pergunta:
   - `[s]ubstituir` — apaga a pasta no alvo e copia a local
   - `[i]gnorar` — deixa intacta
4. **Para cada pasta presente só em `./skills/`** (skill nova), pergunta:
   - `[s]im` — copia a local pro alvo
   - `[n]ão` — não insere
5. Pastas que existem **só no alvo** (não há equivalente local) ficam intocadas — só entram no backup.

## Como rodar

A flag `--target-folder` / `-t` é **obrigatória**. Caminho relativo é resolvido a partir da raiz do repositório.

### Produção — aplicar nas skills reais do Claude

```bash
python3 meta-scripts/apply-skills/apply_skills.py -t ~/.claude/skills
```

### Teste seguro — usar pasta sandbox neste repositório

Use `.example-script-skills/` (gitignored) como alvo. Crie pastas fake lá dentro pra testar os cenários (substituição, inserção, ignorar) sem mexer no seu `~/.claude/skills`.

```bash
python3 meta-scripts/apply-skills/apply_skills.py -t .example-script-skills
```

### Sem perguntar (modo automático)

A flag `--yes` / `-y` aplica tudo sem prompt: substitui todas as existentes e insere todas as novas.

```bash
python3 meta-scripts/apply-skills/apply_skills.py -t ~/.claude/skills --yes
```

## Flags

| Flag | Obrigatório | Descrição |
|------|-------------|-----------|
| `-t`, `--target-folder` | sim | Pasta-alvo a sincronizar. Pode ser absoluto (`~/.claude/skills`) ou relativo à raiz do repositório (`.example-script-skills`). |
| `-y`, `--yes` | não | Aplica tudo sem perguntar. |
| `-h`, `--help` | não | Mostra a ajuda. |

## Onde fica o backup

Sempre em `./backup-skills/<YYYY-MM-DD_HH-MM-SS>/`, relativo à raiz do repositório, independentemente da pasta-alvo escolhida. A pasta `backup-skills/` está no `.gitignore`.

## Pastas envolvidas

- **Origem** (fonte das skills): `./skills/` — sempre.
- **Alvo** (`-t`): obrigatório, definido por flag.
- **Backup**: `./backup-skills/<timestamp>/` — sempre.

## Resumo de fim de execução

Ao terminar, o script imprime:

```
[fim] substituídas: N | inseridas: M | ignoradas: K
```
