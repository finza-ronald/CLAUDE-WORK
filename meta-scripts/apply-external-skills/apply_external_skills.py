#!/usr/bin/env python3
"""Sincroniza skills externas (./external-skills/<sub>) com uma pasta-alvo.

Mesma lógica do apply_skills.py, mas:
- A pasta de origem é parametrizada e fica sob ./external-skills/.
- Útil para aplicar conjuntos de skills de terceiros, ex.:
  ./external-skills/meu-colega-skills/

Fluxo:
1. Faz backup de todas as pastas da pasta-alvo para
   ./backup-skills/<YYYY-MM-DD_HH-MM-SS>/.
2. Lista pastas na pasta-alvo e na pasta de origem (sob ./external-skills/).
3. Para cada pasta presente nos dois lados, pergunta:
   substituir (s) ou ignorar (i).
4. Para cada pasta presente só na origem, pergunta:
   inserir (s) ou não inserir (n).
5. Aplica as ações confirmadas.

Flags:
    --source-folder / -s   Pasta com as skills a aplicar (obrigatório).
                           DEVE iniciar com 'external-skills/'.
                           Ex.: -s external-skills/finza-workspace/skills
    --target-folder / -t   Pasta-alvo a ser sincronizada (obrigatório).
    --yes / -y             Aplica tudo sem perguntar.

Uso:
    python meta-scripts/apply-external-skills/apply_external_skills.py \\
        -s external-skills/finza-workspace/skills -t ~/.claude/skills
"""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
EXTERNAL_SKILLS_ROOT = REPO_ROOT / "external-skills"
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


def confirm_replace(skill_name: str, source_label: str) -> bool:
    return ask(
        f"Skill '{skill_name}' existe nos dois lados (origem: {source_label}). "
        "Substituir? [s]ubstituir / [i]gnorar: ",
        yes_aliases={"s", "substituir"},
        no_aliases={"i", "ignorar"},
    )


def confirm_insert(skill_name: str, source_label: str) -> bool:
    return ask(
        f"Skill '{skill_name}' existe só em {source_label}. "
        "Inserir? [s]im / [n]ão: ",
        yes_aliases={"s", "sim", "inserir"},
        no_aliases={"n", "nao", "não"},
    )


def copy_skill(skill_name: str, source_dir: Path, target_dir: Path) -> None:
    """Copia <source_dir>/<skill_name> para <target_dir>/<skill_name>.

    Se o destino existe, é apagado antes (substituição).
    """
    target = target_dir / skill_name
    source = source_dir / skill_name

    action = "substituída" if target.exists() else "inserida"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)
    print(f"[ok] '{skill_name}' {action} em {target}")


def resolve_source(raw: str) -> Path:
    """Resolve a pasta de origem. Deve iniciar com 'external-skills/'.

    O caminho passado precisa começar literalmente com 'external-skills/'
    (relativo à raiz do repositório). Caminho absoluto ou que não comece
    com esse prefixo é rejeitado.
    """
    candidate = Path(raw)
    if candidate.is_absolute():
        raise ValueError(
            "--source-folder deve iniciar com 'external-skills/' "
            f"(caminho relativo à raiz do repo). Recebido absoluto: {raw}"
        )

    parts = candidate.parts
    if not parts or parts[0] != "external-skills":
        raise ValueError(
            "--source-folder deve iniciar com 'external-skills/'. "
            f"Recebido: '{raw}'. "
            "Ex.: -s external-skills/finza-workspace/skills"
        )

    resolved = (REPO_ROOT / candidate).resolve()
    external_resolved = EXTERNAL_SKILLS_ROOT.resolve()
    if not resolved.is_relative_to(external_resolved):
        raise ValueError(
            f"--source-folder deve ficar sob ./external-skills/, "
            f"resolveu para fora: {resolved}"
        )
    return resolved


def resolve_target(raw: str) -> Path:
    """Resolve a pasta-alvo. Caminho relativo é resolvido a partir do REPO_ROOT."""
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = (REPO_ROOT / path).resolve()
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Sincroniza uma pasta sob ./external-skills/ com uma pasta-alvo."
        ),
    )
    parser.add_argument(
        "-s", "--source-folder",
        required=True,
        help=(
            "Pasta com as skills a aplicar (obrigatório). DEVE iniciar com "
            "'external-skills/'. Ex.: -s external-skills/finza-workspace/skills"
        ),
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

    if not EXTERNAL_SKILLS_ROOT.is_dir():
        print(
            f"[erro] Pasta ./external-skills/ não encontrada em "
            f"{EXTERNAL_SKILLS_ROOT}"
        )
        return 1

    try:
        source_dir = resolve_source(args.source_folder)
    except ValueError as exc:
        print(f"[erro] {exc}")
        return 1

    if not source_dir.is_dir():
        print(
            f"[erro] Pasta de origem não encontrada: {source_dir}\n"
            f"       Verifique se '{args.source_folder}' existe a partir "
            f"da raiz do repositório."
        )
        return 1

    target_dir = resolve_target(args.target_folder)

    source_label = f"./{args.source_folder}"
    print(f"[info] source: {source_dir}")
    print(f"[info] target: {target_dir}")

    target_dir.mkdir(parents=True, exist_ok=True)

    backup_target(target_dir)

    source = set(list_skill_dirs(source_dir))
    remote = set(list_skill_dirs(target_dir))
    common = sorted(source & remote)
    only_source = sorted(source - remote)

    if not common and not only_source:
        print(
            f"[info] Nada para sincronizar — {source_label} está vazia "
            "ou já alinhada."
        )
        return 0

    if common:
        print(f"[info] {len(common)} em comum: {', '.join(common)}")
    if only_source:
        print(f"[info] {len(only_source)} só na origem: {', '.join(only_source)}")

    replaced = 0
    inserted = 0
    ignored = 0

    for skill_name in common:
        if args.yes or confirm_replace(skill_name, source_label):
            copy_skill(skill_name, source_dir, target_dir)
            replaced += 1
        else:
            print(f"[skip] '{skill_name}' ignorada.")
            ignored += 1

    for skill_name in only_source:
        if args.yes or confirm_insert(skill_name, source_label):
            copy_skill(skill_name, source_dir, target_dir)
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
