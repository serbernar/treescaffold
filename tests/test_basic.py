from pathlib import Path
from treescaffold.core import parse_lines, create_structure

EXAMPLE = """\
root/
├── a/
│   └── x.txt
└── b.txt
"""


def test_parse_and_materialize(tmp_path: Path):
    entries = parse_lines(EXAMPLE)
    created_dirs, created_files = create_structure(
        entries, base_dir=tmp_path, dry=False
    )
    print(created_dirs)
    print(created_files)

    assert (tmp_path / "root").is_dir()
    assert (tmp_path / "root/a").is_dir()
    assert (tmp_path / "root/a/x.txt").is_file()
    assert (tmp_path / "root/b.txt").is_file()
    # created sets reflect items
    assert not (
        tmp_path / "root/a/.gitkeep"
    ).exists()  # dir 'a' is non-empty? then .gitkeep may not exist
