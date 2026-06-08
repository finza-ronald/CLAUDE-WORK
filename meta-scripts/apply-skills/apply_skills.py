#!/usr/bin/env python3
"""Sincroniza skills locais (./skills) com uma pasta-alvo.

Fluxo:
1. Faz backup de todas as pastas da pasta-alvo para
   ./backup-skills/<YYYY-MM-DD_HH-MM-SS>/.
2. Lista pastas na pasta-alvo e em ./skills.
3. Para cada pasta presente nos dois lados, pergunta:
   substituir (s) ou ignorar (i).
4. Para cada pasta presente só em ./skills, pergunta:
   inserir (s) ou não inserir (n).
5. Aplica as ações confirmadas.

Flags:
    --target-folder / -t   Pasta-alvo a ser sincronizada (obrigatório).
    --yes / -y             Aplica tudo sem perguntar.
    --new / -n             Só considera skills que mudaram. Compara a
                           estrutura das pastas e o conteúdo dos arquivos
                           (incluindo SKILL.md) entre ./skills e a pasta-alvo;
                           skills idênticas são puladas sem perguntar.

Uso:
    python meta-scripts/apply-skills/apply_skills.py -t ~/.claude/skills
    python meta-scripts/apply-skills/apply_skills.py -t .example-script-skills --yes
    python meta-scripts/apply-skills/apply_skills.py -t .example-script-skills --new
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from datetime import datetime
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
LOCAL_SKILLS_DIR = REPO_ROOT / "skills"
BACKUP_ROOT = REPO_ROOT / "backup-skills"


def is_skill_dir(path: Path) -> bool:
    """Verdadeiro se `path` é uma pasta de skill válida.

    Regras:
    - É uma pasta.
    - O nome não começa com '.'.
    - Tem, imediatamente dentro, um arquivo SKILL.md (case-insensitive).
    """
    if not path.is_dir() or path.name.startswith("."):
        return False
    return any(
        child.is_file() and child.name.lower() == "skill.md"
        for child in path.iterdir()
    )


def list_skill_dirs(base: Path) -> list[str]:
    if not base.is_dir():
        return []
    return sorted(p.name for p in base.iterdir() if is_skill_dir(p))


def skill_changed(source: Path, target: Path) -> bool:
    """Verdadeiro se a skill mudou entre `source` e `target`.

    Compara, de forma recursiva:
    - A estrutura: o conjunto de caminhos relativos (arquivos e subpastas).
    - O conteúdo: byte a byte de cada arquivo (inclui SKILL.md).

    Se o destino não existe, considera que mudou (é nova).
    """
    if not target.exists():
        return True

    source_paths = {p.relative_to(source) for p in source.rglob("*")}
    target_paths = {p.relative_to(target) for p in target.rglob("*")}
    if source_paths != target_paths:
        return True

    for rel in source_paths:
        src_file = source / rel
        if not src_file.is_file():
            continue
        dst_file = target / rel
        if not dst_file.is_file() or not filecmp.cmp(src_file, dst_file, shallow=False):
            return True

    return False


def backup_target(target_dir: Path) -> Path:
    """Copia <target_dir>/* para ./backup-skills/<timestamp>/."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = BACKUP_ROOT / timestamp
    backup_dir.mkdir(parents=True, exist_ok=True)

    if not target_dir.is_dir():
        print(f"[backup] {target_dir} não existe — backup vazio em {backup_dir}")
        return backup_dir

    copied = 0
    for entry in target_dir.iterdir():
        if not entry.is_dir():
            continue
        shutil.copytree(entry, backup_dir / entry.name)
        copied += 1

    print(f"[backup] {copied} skill(s) copiada(s) para {backup_dir}")
    return backup_dir


def ask(prompt: str, yes_aliases: set[str], no_aliases: set[str]) -> bool:
    """Pergunta sim/não com aliases customizados. Enter = não."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in yes_aliases:
            return True
        if answer in no_aliases or answer == "":
            return False
        print("Resposta inválida.")


def confirm_replace(skill_name: str) -> bool:
    return ask(
        f"Skill '{skill_name}' existe nos dois lados. "
        "Substituir? [s]ubstituir / [i]gnorar: ",
        yes_aliases={"s", "substituir"},
        no_aliases={"i", "ignorar"},
    )


def confirm_insert(skill_name: str) -> bool:
    return ask(
        f"Skill '{skill_name}' existe só em ./skills. "
        "Inserir? [s]im / [n]ão: ",
        yes_aliases={"s", "sim", "inserir"},
        no_aliases={"n", "nao", "não"},
    )


def copy_skill(skill_name: str, target_dir: Path) -> None:
    """Copia ./skills/<skill_name> para <target_dir>/<skill_name>.

    Se o destino existe, é apagado antes (substituição).
    """
    target = target_dir / skill_name
    source = LOCAL_SKILLS_DIR / skill_name

    action = "substituída" if target.exists() else "inserida"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)
    print(f"[ok] '{skill_name}' {action} em {target}")


def resolve_target(raw: str) -> Path:
    """Resolve a pasta-alvo. Caminho relativo é resolvido a partir do REPO_ROOT."""
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = (REPO_ROOT / path).resolve()
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sincroniza ./skills com uma pasta-alvo de skills.",
    )
    parser.add_argument(
        "-t", "--target-folder",
        required=True,
        help=(
            "Pasta-alvo a ser sincronizada (obrigatório). "
            "Caminho relativo é resolvido a partir da raiz do repositório. "
            "Ex.: ~/.claude/skills ou .example-script-skills"
        ),
    )
    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Aplica tudo sem perguntar (substitui existentes e insere novas).",
    )
    parser.add_argument(
        "-n", "--new",
        action="store_true",
        help=(
            "Só considera skills que mudaram. Compara estrutura das pastas e "
            "conteúdo dos arquivos (incluindo SKILL.md); pula as idênticas."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target_dir = resolve_target(args.target_folder)

    if not LOCAL_SKILLS_DIR.is_dir():
        print(f"[erro] Pasta local de skills não encontrada: {LOCAL_SKILLS_DIR}")
        return 1

    print(f"[info] target: {target_dir}")
    target_dir.mkdir(parents=True, exist_ok=True)

    local = set(list_skill_dirs(LOCAL_SKILLS_DIR))
    remote = set(list_skill_dirs(target_dir))
    common = sorted(local & remote)
    only_local = sorted(local - remote)

    unchanged = 0
    if args.new:
        changed_common = []
        for skill_name in common:
            if skill_changed(LOCAL_SKILLS_DIR / skill_name, target_dir / skill_name):
                changed_common.append(skill_name)
            else:
                unchanged += 1
        if unchanged:
            print(f"[info] {unchanged} sem alterações (puladas).")
        common = changed_common

    if not common and not only_local:
        print("[info] Nada para sincronizar — nenhuma skill nova ou alterada.")
        return 0

    if common:
        rotulo = "em comum (alteradas)" if args.new else "em comum"
        print(f"[info] {len(common)} {rotulo}: {', '.join(common)}")
    if only_local:
        print(f"[info] {len(only_local)} só local: {', '.join(only_local)}")

    backup_target(target_dir)

    replaced = 0
    inserted = 0
    ignored = 0

    for skill_name in common:
        if args.yes or confirm_replace(skill_name):
            copy_skill(skill_name, target_dir)
            replaced += 1
        else:
            print(f"[skip] '{skill_name}' ignorada.")
            ignored += 1

    for skill_name in only_local:
        if args.yes or confirm_insert(skill_name):
            copy_skill(skill_name, target_dir)
            inserted += 1
        else:
            print(f"[skip] '{skill_name}' não inserida.")
            ignored += 1

    print(
        f"\n[fim] substituídas: {replaced} | "
        f"inseridas: {inserted} | "
        f"ignoradas: {ignored}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
