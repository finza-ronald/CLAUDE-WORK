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

Uso:
    python meta-scripts/apply-skills/apply_skills.py -t ~/.claude/skills
    python meta-scripts/apply-skills/apply_skills.py -t .example-script-skills --yes
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
LOCAL_SKILLS_DIR = REPO_ROOT / "skills"
BACKUP_ROOT = REPO_ROOT / "backup-skills"


def list_skill_dirs(base: Path) -> list[str]:
    if not base.is_dir():
        return []
    return sorted(p.name for p in base.iterdir() if p.is_dir())


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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target_dir = resolve_target(args.target_folder)

    if not LOCAL_SKILLS_DIR.is_dir():
        print(f"[erro] Pasta local de skills não encontrada: {LOCAL_SKILLS_DIR}")
        return 1

    print(f"[info] target: {target_dir}")
    target_dir.mkdir(parents=True, exist_ok=True)

    backup_target(target_dir)

    local = set(list_skill_dirs(LOCAL_SKILLS_DIR))
    remote = set(list_skill_dirs(target_dir))
    common = sorted(local & remote)
    only_local = sorted(local - remote)

    if not common and not only_local:
        print("[info] Nada para sincronizar — ./skills está vazia ou já alinhada.")
        return 0

    if common:
        print(f"[info] {len(common)} em comum: {', '.join(common)}")
    if only_local:
        print(f"[info] {len(only_local)} só local: {', '.join(only_local)}")

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
