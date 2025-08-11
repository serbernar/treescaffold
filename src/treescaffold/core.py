from __future__ import annotations
import re
from pathlib import Path
from typing import List, Tuple

TREE_CHARS = str.maketrans({"│": " ", "├": " ", "└": " ", "─": " ", "┼": " "})

Entry = Tuple[int, str, bool]  # depth, name, is_dir

def parse_lines(spec: str) -> List[Entry]:
    """
    Parse 'tree' formatted text into (depth, name, is_dir).
    Depth is measured in groups of 4 spaces. Directories end with '/'.
    Lines that are blank or start with '#' are ignored.
    Inline comments after '  # ' are also stripped.
    """
    out: List[Entry] = []
    for raw in spec.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.lstrip().startswith("#"):
            continue
        line = re.split(r"\s+#", line, maxsplit=1)[0].rstrip()
        normalized = line.translate(TREE_CHARS)
        leading_spaces = len(normalized) - len(normalized.lstrip(" "))
        depth = leading_spaces // 4
        name = normalized.strip()
        if not name:
            continue
        is_dir = name.endswith("/")
        out.append((depth, name.rstrip("/"), is_dir))
    return out

def create_structure(
    entries: List[Entry],
    base_dir: Path,
    dry: bool = False,
    force: bool = False,
    gitkeep: bool = True,
) -> tuple[list[Path], list[Path]]:
    """
    Materialize parsed entries under base_dir.
    Returns (created_dirs, created_files).
    """
    base_dir = base_dir.resolve()
    stack: List[Path] = []
    created_dirs: List[Path] = []
    created_files: List[Path] = []

    for depth, name, is_dir in entries:
        while len(stack) > depth:
            stack.pop()
        parent = base_dir.joinpath(*stack) if stack else base_dir
        target = parent / name

        if is_dir:
            created_dirs.append(target)
            if not dry:
                target.mkdir(parents=True, exist_ok=True)
            stack.append(Path(name))
        else:
            created_files.append(target)
            if not dry:
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists() and not force:
                    pass
                else:
                    target.write_text("", encoding="utf-8")

    if gitkeep:
        for d in created_dirs:
            try:
                if d.exists() and not any(d.iterdir()):
                    if not dry:
                        (d / ".gitkeep").touch(exist_ok=True)
            except FileNotFoundError:
                continue

    return created_dirs, created_files