# Contributing to Catalyst Center Export Tools

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

1. **Clear title and description**
2. **Steps to reproduce** the issue
3. **Expected behavior**
4. **Actual behavior**
5. **Environment details**:
   - Python version
   - catalystcentersdk version
   - Operating system
   - Catalyst Center version (if known)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:

1. **Clear title and description** of the enhancement
2. **Use case** explaining why this would be useful
3. **Proposed solution** if you have one in mind
4. **Alternatives considered**

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** with clear, focused commits
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Submit a pull request** with a clear description

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Scripts.git
cd Scripts

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if any)
pip install pylint black pytest

# Copy settings template
cp settings.py.example settings.py
# Edit settings.py with your test environment credentials
```

## Code Style

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Use type hints where appropriate

### Example

```python
def get_device_info(catalyst: CatalystCenter, device_id: str) -> Dict[str, Any]:
    """
    Retrieve detailed information for a specific device.
    
    Args:
        catalyst: Connected Catalyst Center client
        device_id: Unique device identifier
        
    Returns:
        Dictionary containing device information
        
    Raises:
        ApiError: If API call fails
    """
    try:
        device = catalyst.device.get_device_by_id(device_id).response
        return device
    except ApiError as e:
        logger.error(f"Failed to retrieve device {device_id}: {e}")
        raise
```

### Code Formatting

Use `black` for code formatting:

```bash
black *.py
```

### Linting

Use `pylint` to check code quality:

```bash
pylint *.py
```

## Testing

### Manual Testing

Before submitting a PR, test your changes:

```bash
# Test connection
python3 catalyst_cli.py test

# Test each script
python3 getSwitches.py -v
python3 withExport.py -v
python3 exportToExcel.py -v

# Test CLI commands
python3 catalyst_cli.py list devices
python3 catalyst_cli.py list switches --count-only
```

### Writing Tests

If adding new functionality, consider adding tests:

```python
# test_utils.py
import unittest
from utils import validate_ip_address

class TestUtils(unittest.TestCase):
    def test_valid_ip(self):
        self.assertTrue(validate_ip_address('192.168.1.1'))
    
    def test_invalid_ip(self):
        self.assertFalse(validate_ip_address('invalid'))
```

## Commit Messages

Write clear, descriptive commit messages:

```
Good:
- "Add Excel export functionality with formatted worksheets"
- "Fix site caching to reduce API calls"
- "Update README with installation instructions"

Avoid:
- "Fix bug"
- "Update"
- "Changes"
```

## Documentation

### Updating Documentation

When making changes, update relevant documentation:

- **README.md**: Installation, quick start, basic usage
- **USAGE.md**: Detailed examples and use cases
- **CHANGELOG.md**: Document all changes
- **Docstrings**: Keep inline documentation current

### Documentation Style

- Use clear, concise language
- Include examples where helpful
- Use proper Markdown formatting
- Add code blocks with syntax highlighting

## Project Structure

```
Scripts/
├── README.md              # Main documentation
├── USAGE.md              # Detailed usage guide
├── CHANGELOG.md          # Version history
├── CONTRIBUTING.md       # This file
├── requirements.txt      # Python dependencies
├── settings.py.example   # Configuration template
├── .gitignore           # Git ignore rules
├── getSwitches.py       # Switch export script
├── withExport.py        # Raw data export script
├── exportToExcel.py     # Excel export script
├── catalyst_cli.py      # Unified CLI tool
└── utils.py             # Shared utilities
```

## Adding New Features

### Guidelines

1. **Keep it modular**: Add reusable functions to `utils.py`
2. **Follow existing patterns**: Match the style of existing code
3. **Add error handling**: Catch and log exceptions appropriately
4. **Add CLI arguments**: Make features accessible via command line
5. **Update documentation**: Add examples to USAGE.md

### Example: Adding a New Export Format

```python
# In withExport.py

def export_to_xml(data: List[Dict], filename: str, data_type: str) -> None:
    """
    Export data to XML file.
    
    Args:
        data: List of data dictionaries
        filename: Output file name
        data_type: Type of data being exported (for logging)
    """
    import xml.etree.ElementTree as ET
    
    root = ET.Element('data')
    for item in data:
        elem = ET.SubElement(root, 'item')
        for key, value in item.items():
            child = ET.SubElement(elem, key)
            child.text = str(value)
    
    tree = ET.ElementTree(root)
    tree.write(filename)
    logger.info(f"Successfully exported {data_type} to {filename}")

# Add to main() function:
if args.format in ['xml', 'all']:
    export_to_xml(switches, output_dir / 'switches.xml', 'switches')
```

## Code Review Process

1. **Submit PR** with clear description
2. **Automated checks** will run (if configured)
3. **Maintainer review** - may request changes
4. **Address feedback** in new commits
5. **Approval and merge** by maintainer

## Questions?

If you have questions about contributing:

1. Check existing issues and documentation
2. Create a new issue with the "question" label
3. Be specific and provide context

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Recognition

Contributors will be acknowledged in:
- Commit history
- Release notes
- Project documentation (if significant contribution)

Thank you for contributing! 🎉
