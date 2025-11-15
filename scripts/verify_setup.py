#!/usr/bin/env python3
"""
Setup Verification Script
Checks code structure and dependencies without requiring database or Docker
"""

import sys
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(msg):
    print(f"{GREEN}✓{RESET} {msg}")

def print_error(msg):
    print(f"{RED}✗{RESET} {msg}")

def print_warning(msg):
    print(f"{YELLOW}⚠{RESET} {msg}")

def print_info(msg):
    print(f"{BLUE}ℹ{RESET} {msg}")

def check_file_exists(file_path, description):
    """Check if a file exists"""
    if Path(file_path).exists():
        print_success(f"{description}: {file_path}")
        return True
    else:
        print_error(f"{description} missing: {file_path}")
        return False

def check_python_import(module_path, description):
    """Check if a Python module can be imported"""
    try:
        __import__(module_path)
        print_success(f"{description} imports successfully")
        return True
    except ImportError as e:
        print_error(f"{description} import failed: {e}")
        return False
    except Exception as e:
        print_warning(f"{description} import warning: {e}")
        return False

def main():
    print("=" * 70)
    print("1NCE IoT Management Dashboard - Setup Verification")
    print("=" * 70)
    print()

    checks_passed = 0
    total_checks = 0

    # Check Python version
    print_info("Checking Python version...")
    total_checks += 1
    if sys.version_info >= (3, 11):
        print_success(f"Python version: {sys.version.split()[0]}")
        checks_passed += 1
    else:
        print_warning(f"Python {sys.version.split()[0]} - Recommended: 3.11+")

    print()
    print_info("Checking project structure...")

    # Essential files
    files_to_check = [
        ("README.md", "README"),
        ("QUICKSTART.md", "Quick Start Guide"),
        ("DEPLOYMENT.md", "Deployment Guide"),
        ("requirements.txt", "Requirements file"),
        ("Dockerfile", "Dockerfile"),
        ("docker-compose.yml", "Docker Compose config"),
        (".env.example", "Environment template"),
        ("src/app.py", "Main application"),
        ("src/config.py", "Configuration module"),
        ("src/database/models.py", "Database models"),
        ("src/database/connection.py", "Database connection"),
        ("src/api/auth_manager.py", "API auth manager"),
        ("src/api/client.py", "API client"),
        ("src/services/data_collector.py", "Data collector service"),
        ("src/services/alert_service.py", "Alert service"),
        ("src/utils/logger.py", "Logger utility"),
        ("scripts/init_db.py", "Database init script"),
        ("scripts/worker.py", "Background worker"),
        ("scripts/test_api.py", "API test script"),
    ]

    for file_path, description in files_to_check:
        total_checks += 1
        if check_file_exists(file_path, description):
            checks_passed += 1

    # Check Streamlit pages
    print()
    print_info("Checking Streamlit pages...")
    pages = [
        "src/pages/1_📊_Overview.py",
        "src/pages/2_📱_SIM_Management.py",
        "src/pages/3_📈_Usage_Analytics.py",
        "src/pages/4_🔔_Alerts.py",
    ]

    for page in pages:
        total_checks += 1
        if check_file_exists(page, f"Page: {Path(page).name}"):
            checks_passed += 1

    # Check Python dependencies (optional - only if installed)
    print()
    print_info("Checking Python dependencies (optional)...")

    dependencies = [
        ("streamlit", "Streamlit"),
        ("sqlalchemy", "SQLAlchemy"),
        ("pandas", "Pandas"),
        ("plotly", "Plotly"),
        ("requests", "Requests"),
        ("pydantic", "Pydantic"),
    ]

    deps_installed = 0
    for module, name in dependencies:
        if check_python_import(module, name):
            deps_installed += 1

    if deps_installed == 0:
        print_warning("No dependencies installed. Run: pip install -r requirements.txt")
    elif deps_installed < len(dependencies):
        print_warning(f"Some dependencies missing ({deps_installed}/{len(dependencies)} installed)")

    # Check .env file
    print()
    print_info("Checking environment configuration...")
    if Path('.env').exists():
        print_success(".env file exists")

        # Check for required variables
        with open('.env', 'r') as f:
            content = f.read()
            required_vars = ['ONENCE_USERNAME', 'ONENCE_PASSWORD', 'DATABASE_URL']
            missing_vars = [var for var in required_vars if var not in content]

            if missing_vars:
                print_warning(f"Missing variables in .env: {', '.join(missing_vars)}")
            else:
                print_success("All required variables present in .env")
    else:
        print_warning(".env file not found. Copy from .env.example and configure")

    # Summary
    print()
    print("=" * 70)
    print(f"Verification Summary: {checks_passed}/{total_checks} checks passed")
    print("=" * 70)
    print()

    if checks_passed == total_checks:
        print_success("All checks passed! Project structure is complete.")
        print()
        print_info("Next steps:")
        print("  1. Configure your .env file with 1NCE credentials")
        print("  2. Choose deployment method:")
        print("     - With Docker: docker-compose up -d")
        print("     - Without Docker: See QUICKSTART.md")
        print("  3. Test API connection: python scripts/test_api.py")
        return 0
    else:
        print_warning(f"Some checks failed ({total_checks - checks_passed} issues)")
        print()
        print_info("This is expected if:")
        print("  - You haven't installed Python dependencies yet")
        print("  - You're planning to use Docker (dependencies install automatically)")
        print()
        print_info("To fix:")
        print("  - Review missing files above")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - See QUICKSTART.md for detailed setup instructions")
        return 1

if __name__ == "__main__":
    sys.exit(main())
