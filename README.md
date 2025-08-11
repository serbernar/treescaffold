# TreeScaffold

A command-line tool to create folder and file structures from tree-spec text files. TreeScaffold parses tree-formatted text (similar to the output of the `tree` command) and materializes the directory structure on disk.

## Features

- 🚀 **Simple and Fast**: Create complex directory structures with a single command
- 📝 **Tree Format**: Uses familiar tree-like text format for easy specification
- 🔧 **Flexible**: Support for comments, dry-run mode, and various options
- 🎯 **Git-Friendly**: Automatically adds `.gitkeep` files to empty directories
- 🛡️ **Safe**: Dry-run mode to preview changes before applying them

## Installation

### From PyPI
```bash
pip install treescaffold
```

### From Source
```bash
git clone https://github.com/serbernar/treescaffold.git
cd treescaffold
pip install -e .
```

## Usage

### Basic Usage

Create a tree specification file (e.g., `project.tree`):

```
my-project/
├── src/
│   ├── main.py
│   └── utils/
│       ├── helpers.py
│       └── config.py
├── tests/
│   └── test_main.py
├── docs/
│   └── README.md
├── requirements.txt
└── .gitignore
```

Then run:
```bash
treescaffold create project.tree
```

### Command Options

```bash
treescaffold create [OPTIONS] SPEC_FILE
```

**Arguments:**
- `SPEC_FILE`: Path to the tree-spec text file

**Options:**
- `--base, -b PATH`: Base directory (default: spec file's parent directory)
- `--dry-run`: Print actions without writing to disk
- `--force`: Overwrite existing files with empty ones
- `--gitkeep/--no-gitkeep`: Place `.gitkeep` into empty directories (default: enabled)

### Examples

#### 1. Create a Python project structure
```bash
# Create a new Python project
treescaffold create examples/jarvis.tree
```

#### 2. Dry run to preview changes
```bash
treescaffold create project.tree --dry-run
```

#### 3. Create structure in a specific directory
```bash
treescaffold create project.tree --base /path/to/target/directory
```

#### 4. Force overwrite existing files
```bash
treescaffold create project.tree --force
```

## Tree Specification Format

TreeScaffold uses a simple tree-like format that's easy to read and write:

### Basic Syntax
- **Directories**: End with `/` (e.g., `src/`, `tests/`)
- **Files**: No trailing slash (e.g., `main.py`, `README.md`)
- **Indentation**: Use 4 spaces for each level of nesting
- **Tree characters**: `├──`, `└──`, `│`, etc. are automatically stripped

### Comments
- Lines starting with `#` are ignored
- Inline comments after `  # ` are stripped
- Blank lines are ignored

### Example Tree File
```
# My Awesome Project
my-project/
├── src/
│   ├── main.py              # Entry point
│   └── utils/
│       ├── helpers.py       # Helper functions
│       └── config.py        # Configuration
├── tests/
│   └── test_main.py         # Unit tests
├── docs/
│   └── README.md            # Documentation
├── requirements.txt         # Dependencies
└── .gitignore              # Git ignore file
```

## API Usage

You can also use TreeScaffold programmatically:

```python
from treescaffold import parse_lines, create_structure
from pathlib import Path

# Parse tree specification
spec_text = """
my-project/
├── src/
│   └── main.py
└── README.md
"""

entries = parse_lines(spec_text)

# Create structure
base_dir = Path("./output")
dirs, files = create_structure(
    entries,
    base_dir=base_dir,
    dry=False,
    force=False,
    gitkeep=True
)

print(f"Created directories: {dirs}")
print(f"Created files: {files}")
```

## Development

### Setup Development Environment

1. Clone the repository:
```bash
git clone https://github.com/serbernar/treescaffold.git
cd treescaffold
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

### Running Tests
```bash
pytest
```

### Code Quality
The project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting:
```bash
ruff check .
ruff format .
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Best Practices

### For Senior Software Engineers

1. **Use TreeScaffold for Project Templates**: Create reusable tree specifications for common project structures (React apps, Python packages, etc.)

2. **Version Control Integration**:
   - Commit your tree specification files to version control
   - Use `--dry-run` before applying changes to production environments
   - Leverage the automatic `.gitkeep` feature for maintaining empty directories

3. **CI/CD Integration**:
   - Use TreeScaffold in build scripts to ensure consistent project structure
   - Validate project structure in CI pipelines

4. **Documentation**:
   - Include comments in tree files to explain the purpose of each directory/file
   - Document the tree specification format for your team

5. **Error Handling**:
   - Always use `--dry-run` first to preview changes
   - Use `--force` carefully, especially in automated scripts
   - Consider backing up existing structures before applying changes

6. **Maintainability**:
   - Keep tree specifications modular and reusable
   - Use consistent naming conventions across your tree files
   - Consider creating a library of common tree patterns for your organization
