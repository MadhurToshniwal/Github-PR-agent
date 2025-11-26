#!/usr/bin/env python3
"""
Setup verification script for PR Review Agent
Checks if everything is configured correctly
"""

import sys
import os
from pathlib import Path
import subprocess


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")


def print_success(text):
    print(f"{Colors.GREEN}✓{Colors.END} {text}")


def print_error(text):
    print(f"{Colors.RED}✗{Colors.END} {text}")


def print_warning(text):
    print(f"{Colors.YELLOW}⚠{Colors.END} {text}")


def check_python_version():
    """Check Python version"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    if version >= (3, 11):
        print_success(f"Python {version.major}.{version.minor}.{version.micro} installed")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor}.{version.micro} found, but 3.11+ required")
        return False


def check_files_exist():
    """Check if required files exist"""
    print_header("Checking Required Files")
    
    required_files = [
        "requirements.txt",
        "app/main.py",
        "app/config.py",
        "app/agents/orchestrator.py",
        ".env.example"
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print_success(f"{file} exists")
        else:
            print_error(f"{file} missing")
            all_exist = False
    
    return all_exist


def check_env_file():
    """Check environment file"""
    print_header("Checking Environment Configuration")
    
    if not Path(".env").exists():
        print_warning(".env file not found")
        print("  Creating from .env.example...")
        
        if Path(".env.example").exists():
            import shutil
            shutil.copy(".env.example", ".env")
            print_success(".env created")
            print_warning("Please edit .env and add your API keys")
            return False
        else:
            print_error(".env.example not found")
            return False
    
    # Check if API key is set
    with open(".env", "r") as f:
        content = f.read()
        
    if "your-openai-api-key" in content or "OPENAI_API_KEY=" not in content:
        print_warning("OPENAI_API_KEY not configured in .env")
        return False
    
    print_success(".env file configured")
    return True


def check_dependencies():
    """Check if dependencies are installed"""
    print_header("Checking Dependencies")
    
    try:
        import fastapi
        print_success(f"fastapi {fastapi.__version__} installed")
    except ImportError:
        print_error("fastapi not installed")
        print("  Run: pip install -r requirements.txt")
        return False
    
    try:
        import openai
        print_success(f"openai installed")
    except ImportError:
        print_error("openai not installed")
        return False
    
    try:
        import pydantic
        print_success(f"pydantic installed")
    except ImportError:
        print_error("pydantic not installed")
        return False
    
    return True


def check_project_structure():
    """Check project structure"""
    print_header("Checking Project Structure")
    
    required_dirs = [
        "app",
        "app/agents",
        "app/services",
        "tests",
        "static"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print_success(f"{dir_path}/ exists")
        else:
            print_error(f"{dir_path}/ missing")
            all_exist = False
    
    return all_exist


def test_import():
    """Test importing the application"""
    print_header("Testing Application Import")
    
    try:
        from app import main
        print_success("Main application imports successfully")
        return True
    except Exception as e:
        print_error(f"Failed to import application: {str(e)}")
        return False


def run_tests():
    """Run test suite"""
    print_header("Running Tests")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success("All tests passed")
            return True
        else:
            print_warning("Some tests failed")
            print(result.stdout)
            return False
    except Exception as e:
        print_warning(f"Could not run tests: {str(e)}")
        return False


def check_docker():
    """Check Docker availability"""
    print_header("Checking Docker (Optional)")
    
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success(f"Docker installed: {result.stdout.strip()}")
            return True
        else:
            print_warning("Docker not available")
            return False
    except:
        print_warning("Docker not installed (optional)")
        return False


def main():
    """Main verification function"""
    print(f"\n{Colors.BLUE}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     PR Review Agent - Setup Verification Tool           ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    checks = []
    
    # Run all checks
    checks.append(("Python Version", check_python_version()))
    checks.append(("Required Files", check_files_exist()))
    checks.append(("Project Structure", check_project_structure()))
    checks.append(("Dependencies", check_dependencies()))
    checks.append(("Environment Config", check_env_file()))
    checks.append(("Application Import", test_import()))
    checks.append(("Tests", run_tests()))
    checks.append(("Docker", check_docker()))
    
    # Summary
    print_header("Verification Summary")
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    for name, result in checks:
        if result:
            print_success(f"{name}: OK")
        else:
            print_error(f"{name}: FAILED")
    
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"Results: {passed}/{total} checks passed")
    
    if passed == total:
        print(f"\n{Colors.GREEN}🎉 All checks passed! Your setup is ready.{Colors.END}")
        print(f"\n{Colors.BLUE}Next steps:{Colors.END}")
        print("  1. Review your .env file")
        print("  2. Run: python start.py")
        print("  3. Visit: http://localhost:8000")
        return 0
    elif passed >= total - 2:
        print(f"\n{Colors.YELLOW}⚠ Setup mostly complete. Review warnings above.{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.RED}❌ Setup incomplete. Please fix errors above.{Colors.END}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
