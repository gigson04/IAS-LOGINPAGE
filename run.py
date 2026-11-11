"""Set up and run the IAS Login System on Windows or macOS."""

import os
from pathlib import Path
import subprocess
import sys
import secrets


ROOT = Path(__file__).resolve().parent
VENV = ROOT / ".venv"
REQUIREMENTS = ROOT / "login" / "requirements.txt"


def main():
    if not VENV.exists():
        print("Creating the project's Python environment...")
        subprocess.check_call([sys.executable, "-m", "venv", str(VENV)], cwd=ROOT)

    python = VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not python.exists():
        raise SystemExit(f"Could not find the virtual environment Python at {python}")

    module_check = (
        "import importlib.util, sys; "
        "sys.exit(0 if all(importlib.util.find_spec(name) for name in "
        "('flask', 'flask_wtf', 'flask_limiter')) else 1)"
    )
    dependencies_missing = subprocess.run(
        [str(python), "-c", module_check], cwd=ROOT, check=False
    ).returncode != 0
    if dependencies_missing:
        print("Installing the project's dependencies...")
        subprocess.check_call(
            [str(python), "-m", "pip", "install", "-r", str(REQUIREMENTS)],
            cwd=ROOT,
        )

    env = os.environ.copy()
    if not env.get("FLASK_SECRET_KEY"):
        env["FLASK_SECRET_KEY"] = secrets.token_urlsafe(48)
    print("Starting the app at http://127.0.0.1:5000 (press Ctrl+C to stop).")
    subprocess.call(
        [str(python), "-m", "flask", "--app", "login.app", "run", "--debug"],
        cwd=ROOT,
        env=env,
    )


if __name__ == "__main__":
    main()
