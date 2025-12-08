"""
Dependency Fixer - Ensures all packages are installed correctly
"""
import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print(f"✅ {package} installed successfully")

def main():
    print("=" * 60)
    print("LinkedIn Agent - Dependency Installer")
    print("=" * 60)
    print(f"Python executable: {sys.executable}")
    print()
    
    packages = [
        "beautifulsoup4",
        "lxml",
        "aiohttp",
        "langchain",
        "langchain-google-genai",
        "pydantic"
    ]
    
    for package in packages:
        try:
            install_package(package)
        except Exception as e:
            print(f"❌ Failed to install {package}: {e}")
    
    print()
    print("=" * 60)
    print("Testing imports...")
    print("=" * 60)
    
    # Test imports
    try:
        from bs4 import BeautifulSoup
        print("✅ bs4 (BeautifulSoup) - OK")
    except ImportError as e:
        print(f"❌ bs4 - FAILED: {e}")
    
    try:
        import aiohttp
        print("✅ aiohttp - OK")
    except ImportError as e:
        print(f"❌ aiohttp - FAILED: {e}")
    
    try:
        import langchain
        print("✅ langchain - OK")
    except ImportError as e:
        print(f"❌ langchain - FAILED: {e}")
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ langchain-google-genai - OK")
    except ImportError as e:
        print(f"❌ langchain-google-genai - FAILED: {e}")
    
    try:
        import pydantic
        print("✅ pydantic - OK")
    except ImportError as e:
        print(f"❌ pydantic - FAILED: {e}")
    
    print()
    print("=" * 60)
    print("All dependencies checked!")
    print("=" * 60)

if __name__ == "__main__":
    main()
