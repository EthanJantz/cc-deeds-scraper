#!/usr/bin/env python3
"""Test runner script for the scraper"""

import sys
import os
import subprocess
from pathlib import Path


def main():
    """Run the test suite"""
    # Add the current directory to Python path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    # Set up environment for testing
    os.environ.setdefault('DB_URL', 'sqlite:///:memory:')
    
    # Run pytest with appropriate arguments
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/',
        '-v',
        '--tb=short',
        '--disable-warnings',
        '--color=yes'
    ]
    
    # Add coverage if available
    try:
        import coverage
        cmd.extend(['--cov=scrape', '--cov-report=term-missing'])
    except ImportError:
        print("Coverage not available, running tests without coverage")
    
    # Run the tests
    result = subprocess.run(cmd, cwd=current_dir)
    
    return result.returncode


if __name__ == '__main__':
    sys.exit(main()) 