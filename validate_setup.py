#!/usr/bin/env python3
"""
Setup Validation Tool for Catalyst Center Export Scripts.

This script validates that all dependencies are installed and the configuration
is correct before running the main export scripts.
"""

import sys
import importlib
from pathlib import Path

# ANSI color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header(text):
    """Print a formatted header."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text.center(60)}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")


def print_success(text):
    """Print a success message."""
    print(f"{GREEN}✓{RESET} {text}")


def print_error(text):
    """Print an error message."""
    print(f"{RED}✗{RESET} {text}")


def print_warning(text):
    """Print a warning message."""
    print(f"{YELLOW}⚠{RESET} {text}")


def check_python_version():
    """Check Python version."""
    print_header("Python Version Check")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 7:
        print_success(f"Python version: {version_str}")
        return True
    else:
        print_error(f"Python version: {version_str}")
        print_error("Python 3.7 or higher is required")
        return False


def check_dependencies():
    """Check if all required dependencies are installed."""
    print_header("Dependency Check")
    
    dependencies = {
        'catalystcentersdk': 'Catalyst Center SDK (required)',
        'openpyxl': 'Excel export support (optional)',
    }
    
    all_required_installed = True
    optional_available = True
    
    for module, description in dependencies.items():
        try:
            importlib.import_module(module)
            print_success(f"{description}: Installed")
        except ImportError:
            if 'optional' in description.lower():
                print_warning(f"{description}: Not installed")
                optional_available = False
            else:
                print_error(f"{description}: Not installed")
                all_required_installed = False
    
    if not all_required_installed:
        print(f"\n{RED}Install missing dependencies with:{RESET}")
        print("    pip install -r requirements.txt")
    
    if not optional_available:
        print(f"\n{YELLOW}Optional features available:{RESET}")
        print("    pip install openpyxl  # For Excel export")
    
    return all_required_installed


def check_configuration():
    """Check if settings.py exists and is properly configured."""
    print_header("Configuration Check")
    
    settings_file = Path('settings.py')
    example_file = Path('settings.py.example')
    
    if not example_file.exists():
        print_warning("settings.py.example not found")
    else:
        print_success("settings.py.example found")
    
    if not settings_file.exists():
        print_error("settings.py not found")
        print(f"\n{YELLOW}Create settings.py from template:{RESET}")
        print("    cp settings.py.example settings.py")
        print("    # Then edit settings.py with your credentials")
        return False
    
    print_success("settings.py found")
    
    # Try to import and validate settings
    try:
        from settings import CATALYST_USERNAME, CATALYST_PASSWORD, CATALYST_BASE_URL
        
        if CATALYST_USERNAME == "your_username_here":
            print_error("CATALYST_USERNAME not configured (still using default)")
            return False
        else:
            print_success(f"CATALYST_USERNAME configured: {CATALYST_USERNAME}")
        
        if CATALYST_PASSWORD == "your_password_here":
            print_error("CATALYST_PASSWORD not configured (still using default)")
            return False
        else:
            print_success("CATALYST_PASSWORD configured: ********")
        
        if CATALYST_BASE_URL == "https://your-catalyst-center.example.com":
            print_error("CATALYST_BASE_URL not configured (still using default)")
            return False
        else:
            print_success(f"CATALYST_BASE_URL configured: {CATALYST_BASE_URL}")
        
        return True
        
    except ImportError as e:
        print_error(f"Failed to import settings: {e}")
        return False
    except AttributeError as e:
        print_error(f"Missing configuration in settings.py: {e}")
        return False


def check_scripts():
    """Check if all main scripts exist."""
    print_header("Script Files Check")
    
    scripts = [
        'getSwitches.py',
        'withExport.py',
        'exportToExcel.py',
        'catalyst_cli.py',
        'utils.py',
    ]
    
    all_present = True
    for script in scripts:
        if Path(script).exists():
            print_success(f"{script} found")
        else:
            print_error(f"{script} not found")
            all_present = False
    
    return all_present


def check_documentation():
    """Check if documentation files exist."""
    print_header("Documentation Check")
    
    docs = [
        'README.md',
        'USAGE.md',
        'CHANGELOG.md',
        'CONTRIBUTING.md',
    ]
    
    for doc in docs:
        if Path(doc).exists():
            print_success(f"{doc} found")
        else:
            print_warning(f"{doc} not found")


def test_connection():
    """Test connection to Catalyst Center (optional)."""
    print_header("Connection Test (Optional)")
    
    response = input("Would you like to test the connection to Catalyst Center? (y/n): ")
    
    if response.lower() != 'y':
        print_warning("Skipping connection test")
        return True
    
    try:
        from utils import load_settings, connect_to_catalyst, get_all_devices
        
        print("\nAttempting to connect...")
        username, password, base_url = load_settings()
        catalyst = connect_to_catalyst(username, password, base_url)
        
        print("Connection successful! Testing API call...")
        devices = get_all_devices(catalyst)
        
        print_success(f"Connected successfully! Found {len(devices)} devices")
        return True
        
    except ImportError as e:
        print_error(f"Cannot test connection - missing dependencies: {e}")
        return False
    except SystemExit:
        print_error("Connection test failed - check your credentials and network")
        return False
    except Exception as e:
        print_error(f"Connection test failed: {e}")
        return False


def main():
    """Main validation function."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{'Catalyst Center Export Tools - Setup Validation'.center(60)}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    results = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'Configuration': check_configuration(),
        'Scripts': check_scripts(),
    }
    
    # Documentation check doesn't affect overall status
    check_documentation()
    
    # Connection test is optional
    if all(results.values()):
        test_connection()
    
    # Summary
    print_header("Validation Summary")
    
    all_passed = True
    for check, passed in results.items():
        if passed:
            print_success(f"{check}: PASSED")
        else:
            print_error(f"{check}: FAILED")
            all_passed = False
    
    if all_passed:
        print(f"\n{GREEN}{'='*60}{RESET}")
        print(f"{GREEN}{'All checks passed! You are ready to go.'.center(60)}{RESET}")
        print(f"{GREEN}{'='*60}{RESET}\n")
        
        print("Next steps:")
        print("  1. Test connection: python3 catalyst_cli.py test")
        print("  2. List devices: python3 catalyst_cli.py list devices")
        print("  3. Export data: python3 getSwitches.py")
        print("  4. See USAGE.md for more examples")
        
        return 0
    else:
        print(f"\n{RED}{'='*60}{RESET}")
        print(f"{RED}{'Some checks failed. Please fix the issues above.'.center(60)}{RESET}")
        print(f"{RED}{'='*60}{RESET}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
