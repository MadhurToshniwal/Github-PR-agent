#!/usr/bin/env python3
"""
Quick start script for PR Review Agent
"""

import subprocess
import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.11+"""
    if sys.version_info < (3, 11):
        print("❌ Python 3.11 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print("✅ Python version OK")


def check_env_file():
    """Check if .env file exists"""
    if not Path(".env").exists():
        print("⚠️  .env file not found")
        print("Creating .env from .env.example...")
        
        if Path(".env.example").exists():
            with open(".env.example", "r") as src:
                content = src.read()
            with open(".env", "w") as dst:
                dst.write(content)
            print("✅ Created .env file")
            print("⚠️  Please edit .env and add your API keys")
            return False
        else:
            print("❌ .env.example not found")
            sys.exit(1)
    print("✅ .env file exists")
    return True


def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True
        )
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)


def run_tests():
    """Run tests"""
    print("🧪 Running tests...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v"],
            check=True
        )
        print("✅ Tests passed")
    except subprocess.CalledProcessError:
        print("⚠️  Some tests failed")
        return False
    return True


def start_server():
    """Start the FastAPI server"""
    print("\n" + "="*50)
    print("🚀 Starting PR Review Agent...")
    print("="*50)
    print("\n📡 API will be available at:")
    print("   - http://localhost:8000")
    print("   - API Docs: http://localhost:8000/docs")
    print("   - Demo UI: http://localhost:8000")
    print("\n⏹️  Press Ctrl+C to stop the server\n")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"],
            check=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
    except subprocess.CalledProcessError:
        print("❌ Failed to start server")
        sys.exit(1)


def main():
    """Main setup and run function"""
    print("🤖 PR Review Agent - Quick Start")
    print("="*50 + "\n")
    
    # Check Python version
    check_python_version()
    
    # Check environment file
    env_ready = check_env_file()
    if not env_ready:
        print("\n⚠️  Please edit .env file and run this script again")
        sys.exit(0)
    
    # Install dependencies
    install_dependencies()
    
    # Ask if user wants to run tests
    print("\n")
    response = input("🧪 Run tests before starting? (y/N): ").lower()
    if response == 'y':
        run_tests()
    
    # Start server
    print("\n")
    response = input("🚀 Start the server? (Y/n): ").lower()
    if response != 'n':
        start_server()


if __name__ == "__main__":
    main()
