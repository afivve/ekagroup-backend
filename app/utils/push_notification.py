from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests
import os

# Masukkan path ke file JSON kredensial
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Direktori saat file ini berada
CREDENTIALS_FILE = os.path.join(BASE_DIR, "notif-practice.json")

# URL API HTTP v1
FCM_URL = "https://fcm.googleapis.com/v1/projects/notif-practice-74169/messages:send"

# Membaca kredensial dari file JSON
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_FILE,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)


async def push_notification(token: str, title: str, body: str):
    """
    Fungsi untuk mengirim notifikasi menggunakan Firebase Cloud Messaging (FCM).

    Args:
        token (str): Token perangkat tujuan.
        title (str): Judul notifikasi.
        body (str): Isi notifikasi.

    Returns:
        dict: Response dari FCM.
    """
    # Periksa apakah token masih valid
    if not credentials.valid or credentials.expired:
        credentials.refresh(Request())

    access_token = credentials.token

    # Payload untuk FCM
    payload = {
        "message": {
            "token": token,
            "notification": {
                "title": title,
                "body": body,
            },
        }
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Mengirim permintaan POST ke FCM
    response = requests.post(FCM_URL, json=payload, headers=headers)
    return response.json()
