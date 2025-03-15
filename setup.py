import sys
import os
import subprocess

# Check Python version
MIN_PYTHON_VERSION = (3, 7)
if sys.version_info < MIN_PYTHON_VERSION:
    print("Python 3.7 or higher is required. Please install it before running this script.")
    sys.exit(1)

# Define virtual environment directory
VENV_DIR = "venv"

# Create virtual environment if it doesn't exist
if not os.path.exists(VENV_DIR):
    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", VENV_DIR])
else:
    print("Virtual environment already exists.")

# Activate virtual environment
if os.name == "nt":  # Windows
    activate_script = os.path.join(VENV_DIR, "Scripts", "activate")
else:  # Linux/macOS
    activate_script = os.path.join(VENV_DIR, "bin", "activate")

# Ensure activation script exists
if not os.path.exists(activate_script):
    print("Error: Virtual environment activation script not found!")
    sys.exit(1)

print(f"Activating virtual environment: {activate_script}")

# Install dependencies from requirements.txt
requirements_file = "requirements.txt"
if os.path.exists(requirements_file):
    print("Installing dependencies...")
    subprocess.run([os.path.join(VENV_DIR, "bin" if os.name != "nt" else "Scripts", "python"), "-m", "pip", "install", "-r", requirements_file])
    print("Dependencies installed successfully.")
else:
    print("No requirements.txt file found. Skipping dependency installation.")

print("Setup complete!")