import subprocess
import time
import requests
import webbrowser
import os
import sys

BACKEND_URL = "http://127.0.0.1:8000/docs"
FRONTEND_URL = "http://localhost:8501"


def banner():
    print("=" * 55)
    print("        🚀 LeetRecall AI Launcher v1.0")
    print("=" * 55)
    print()


def start_backend():

    print("[1/4] Starting FastAPI Backend...")

    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.main:app",
            "--reload"
        ]
    )


def wait_for_backend():

    print("[2/4] Waiting for backend...")

    while True:

        try:

            requests.get(
                BACKEND_URL,
                timeout=1
            )

            print("✓ Backend is ready.\n")

            break

        except Exception:

            time.sleep(1)


def start_frontend():

    print("[3/4] Starting Streamlit...")

    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "frontend/app.py"
        ]
    )


def open_browser():

    print("[4/4] Opening browser...\n")

    time.sleep(5)

    webbrowser.open(FRONTEND_URL)


if __name__ == "__main__":

    os.chdir(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    banner()

    backend = start_backend()

    wait_for_backend()

    start_frontend()

    open_browser()

    print("=" * 55)
    print("Application Ready!")
    print("=" * 55)
    print()
    print("Backend :", BACKEND_URL)
    print("Frontend:", FRONTEND_URL)
    print()
    print("Press CTRL+C to exit launcher.")
    print()

try:
    backend.wait()

except KeyboardInterrupt:

    print("\n\nStopping LeetRecall AI...")

    backend.terminate()

    os.system("taskkill /F /IM streamlit.exe >nul 2>&1")
    os.system("taskkill /F /IM python.exe >nul 2>&1")

    print("✓ Backend stopped.")
    print("✓ Frontend stopped.")
    print("Goodbye!")