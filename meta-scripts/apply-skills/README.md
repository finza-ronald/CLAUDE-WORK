# apply-skills

Script para sincronizar as skills locais do repositório (`./skills/`) com uma pasta-alvo — geralmente `~/.claude/skills`, mas pode ser qualquer pasta (útil pra testar antes em uma pasta sandbox).

## O que o script faz

1. **Compara** os nomes de pastas em `./skills/` e em `<target-folder>/` (com `--new`, compara também estrutura e conteúdo para detectar o que mudou).
2. **Backup antes de aplicar.** Havendo algo a sincronizar, copia tudo de `<target-folder>/*` para `./backup-skills/<YYYY-MM-DD_HH-MM-SS>/` antes de qualquer escrita. (Com `--new` sem mudanças, não cria backup.)
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

### Só o que mudou (modo incremental)

A flag `--new` / `-n` compara cada skill em comum entre `./skills/` e o alvo, considerando **estrutura das pastas** (conjunto de arquivos e subpastas) e **conteúdo dos arquivos** byte a byte — incluindo o `SKILL.md` (case-insensitive). Skills idênticas são puladas sem perguntar; só as alteradas entram no fluxo de substituição. Skills novas (só em `./skills/`) continuam sendo oferecidas para inserção.

Útil pra, depois de editar uma skill, aplicar no Claude apenas a pasta que mudou — sem reaplicar (nem fazer backup à toa) o que está igual.

```bash
# pergunta só pelas alteradas
python3 meta-scripts/apply-skills/apply_skills.py -t ~/.claude/skills --new

# aplica direto só as alteradas
python3 meta-scripts/apply-skills/apply_skills.py -t ~/.claude/skills --new --yes
```

Quando `--new` não encontra nenhuma skill nova ou alterada, o script não cria backup e encerra com `Nada para sincronizar`.

## Flags

| Flag | Obrigatório | Descrição |
|------|-------------|-----------|
| `-t`, `--target-folder` | sim | Pasta-alvo a sincronizar. Pode ser absoluto (`~/.claude/skills`) ou relativo à raiz do repositório (`.example-script-skills`). |
| `-y`, `--yes` | não | Aplica tudo sem perguntar. |
| `-n`, `--new` | não | Só considera skills que mudaram (compara estrutura e conteúdo, incluindo `SKILL.md`); pula as idênticas. Combina com `--yes`. |
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
