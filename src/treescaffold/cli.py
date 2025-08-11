from __future__ import annotations
from pathlib import Path
import typer
from .core import parse_lines, create_structure

app = typer.Typer(add_completion=False, help="Create folders/files from a tree-spec text file.")

@app.command()
def create(
    spec_file: Path = typer.Argument(..., exists=True, readable=True, help="Tree-spec text file."),
    base: Path = typer.Option(None, "--base", "-b", help="Base directory (default: spec file's parent)."),
    dry: bool = typer.Option(False, "--dry-run", help="Print actions without writing to disk."),
    force: bool = typer.Option(False, "--force", help="Overwrite existing files with empty ones."),
    gitkeep: bool = typer.Option(True, "--gitkeep/--no-gitkeep", help="Place .gitkeep into empty dirs."),
):
    spec_text = spec_file.read_text(encoding="utf-8")
    entries = parse_lines(spec_text)
    base_dir = base if base is not None else spec_file.parent

    dirs, files = create_structure(entries, base_dir=base_dir, dry=dry, force=force, gitkeep=gitkeep)

    typer.echo(f"Base: {base_dir.resolve()}")
    if dry:
        typer.echo("Dry-run; nothing written.\n")
    typer.echo("Directories:")
    for d in dirs:
        typer.echo(f"  {d}")
    typer.echo("\nFiles:")
    for f in files:
        typer.echo(f"  {f}")