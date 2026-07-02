import requests

# Change this to your Render backend URL when deploying
import os

API_BASE = os.getenv(
    "API_BASE",
    "http://127.0.0.1:8000"
)


def login(email: str, password: str):
    """
    Login user.
    """

    try:
        response = requests.post(
            f"{API_BASE}/auth/login",
            json={
                "email": email,
                "password": password
            },
            timeout=20
        )

        return response.json()

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "message": "Cannot connect to backend."
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }


def signup(username: str, email: str, password: str):
    """
    Register user.
    """

    try:

        response = requests.post(
            f"{API_BASE}/auth/signup",
            json={
                "username": username,
                "email": email,
                "password": password
            },
            timeout=20
        )

        return response.json()

    except requests.exceptions.ConnectionError:

        return {
            "success": False,
            "message": "Cannot connect to backend."
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }