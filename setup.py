import os
import platform
import subprocess
import venv

VENV_DIR = ".venv"


def main() -> None:
    if not os.path.exists(VENV_DIR):
        venv.create(VENV_DIR, with_pip=True)

    if platform.system().lower() == "windows":
        venv_python = os.path.join(VENV_DIR, "Scripts", "python.exe")
        venv_pip = os.path.join(VENV_DIR, "Scripts", "pip.exe")
    else:
        venv_python = os.path.join(VENV_DIR, "bin", "python")
        venv_pip = os.path.join(VENV_DIR, "bin", "pip")

    upgrade_args = [
        venv_python,
        "-m",
        "pip",
        "install",
        "--upgrade",
        "pip",
    ]
    subprocess.run(upgrade_args, check=True)

    if os.path.exists("requirements.txt"):
        req_args = [venv_pip, "install", "-r", "requirements.txt"]
        subprocess.run(req_args, check=True)


if __name__ == "__main__":
    main()
