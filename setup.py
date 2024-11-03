import subprocess
import sys

def install_requirements():
    """Installs packages from requirements.txt."""
    try:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to install packages:", e)

if __name__ == "__main__":
    install_requirements()
