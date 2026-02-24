# AGENTS.md - Development Guidelines for AI Agents

## Project Overview

This is a Chinese-language CHM to Markdown conversion tool. It:
1. Extracts CHM files using 7-zip to an `html/` folder
2. Converts HTML files to Markdown in a `md/` folder
3. Handles image extraction and cross-CHM link conversion

## Project Structure

```
.
├── scripts/           # Main Python scripts
│   ├── config.py     # Configuration (7-zip paths)
│   ├── ui.py         # GUI folder selection dialog
│   ├── extract.py    # CHM extraction using 7-zip
│   ├── convert.py   # HTML to Markdown conversion
│   └── main.py      # Entry point
├── test_source/      # Test data (small CHM files)
├── J750_HELP/        # Full CHM files for testing
├── PLAN.md           # Project specification
└── AGENTS.md         # This file
```

## Build/Lint/Test Commands

### Running the Application

```bash
# Run the main script (opens GUI folder picker)
python3 scripts/main.py

# Or run with specific Python path
D:/Download/pyenv-win/pyenv/pyenv-win/versions/3.10.5/python.exe scripts/main.py
```

### Syntax Checking

```bash
# Check all Python files for syntax errors
python3 -m py_compile scripts/config.py scripts/ui.py scripts/extract.py scripts/convert.py scripts/main.py

# Or check a single file
python3 -m py_compile scripts/convert.py
```

### Testing

This project uses manual testing with test data:
- `test_source/` - Small CHM files for quick testing
- `J750_HELP/` - Full CHM files for comprehensive testing

To test a single function:
```bash
python3 -c "
import sys
sys.path.insert(0, 'scripts')
from convert import html_to_md
from pathlib import Path

html_path = Path('test_source/html/APMU/APMUDefTopic.html')
md_path = Path('test_source/md/APMU/APMUDefTopic.md')
base_dir = Path('test_source/html')
md_dir = Path('test_source/md')
images_dir = Path('test_source/md/images')

html_to_md(html_path, md_path, base_dir, md_dir, images_dir)
"
```

### Installing Dependencies

```bash
# Install html2text (required)
pip3 install html2text

# Or with specific Python
D:/Download/pyenv-win/pyenv/pyenv-win/versions/3.10.5/python.exe -m pip install html2text
```

## Code Style Guidelines

### Imports

- Standard library imports first, then third-party, then local
- Use absolute imports: `from config import SEVEN_ZIP`
- Group by: `os/re` (built-in) → `html2text` (third-party) → `scripts modules`

```python
import os
import re
import shutil
from pathlib import Path
import html2text
```

### Formatting

- Line length: 100 characters max
- Indentation: 4 spaces (not tabs)
- Use blank lines to separate logical sections (2 blank lines between functions)
- No trailing whitespace

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Functions | snake_case | `html_to_md`, `extract_chm` |
| Variables | snake_case | `html_path`, `md_dir` |
| Classes | PascalCase | (not used in this project) |
| Constants | UPPER_SNAKE | `SEVEN_ZIP_PATHS` |
| Files | snake_case | `extract.py`, `convert.py` |

### Type Annotations

Recommended but not strictly required. When used:
```python
def html_to_md(html_path: Path, md_path: Path, base_dir: Path, md_dir: Path, images_dir: Path) -> None:
```

### Error Handling

- Use `errors='ignore'` when reading potentially malformed HTML files
- Use try/except for file operations that may fail
- Provide meaningful error messages

```python
with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    html_content = f.read()
```

### Path Handling

- Always use `pathlib.Path` for path operations (not os.path)
- Use `/` operator for path joining: `md_dir / target_chm_name / md_file`
- Be careful with variable name reuse (e.g., don't reassign `md_dir` after it's passed as parameter)

```python
# Good
from pathlib import Path
target_path = md_dir / target_chm_name / md_file

# Avoid
import os
target_path = os.path.join(md_dir, target_chm_name, md_file)
```

### String Handling

- Use f-strings for string formatting
- Handle both forward and backslashes in paths:
```python
rel_path = os.path.relpath(target_path, current_path).replace(os.sep, '/')
```

### Working with Windows

- This project runs on Windows, use `os.sep` for path separator
- 7-zip default paths:
  - `C:\Program Files\7-Zip\7z.exe`
  - `C:\Program Files (x86)\7-Zip\7z.exe`

### HTML Processing Notes

When modifying convert.py, be aware of:
1. Order matters: process `chm_link_pattern` (chm://, ms-its:) BEFORE `a_pattern` (regular links)
2. html2text may convert relative paths differently than expected
3. Test with actual CHM files in test_source/

## Common Tasks

### Adding a New Conversion Rule

1. Edit `scripts/convert.py`
2. Find the appropriate function (`html_to_md` or `convert_folder`)
3. Add your regex pattern and replacement logic
4. Test with: `python3 scripts/main.py` and select test_source folder

### Debugging Link Conversion

Add print statements:
```python
print(f"DEBUG: rel_path={rel_path}")
```

Then run on test_source and check the generated md files.

### Running Full Conversion

```bash
# This opens GUI folder picker
python3 scripts/main.py

# Then manually verify output in the md/ folder
```

## Important Notes

1. The test_source folder contains small CHM files for testing
2. Always verify output MD files have correct relative paths for images and links
3. Cross-CHM links (ms-its:) need `../` prefix for relative paths
4. Variable name shadowing: don't reuse `md_dir` variable inside functions
