from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from typing import Dict
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        # Menyimpan koneksi aktif berdasarkan user_id
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logging.info(
            f"User {user_id} connected. Active connections: {list(self.active_connections.keys())}"
        )

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logging.info(
                f"User {user_id} disconnected. Active connections: {list(self.active_connections.keys())}"
            )

    async def send_personal_message(self, message: dict, user_id: str):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_json(message)
            logging.info(f"Message sent to user {user_id}: {message}")
        else:
            logging.warning(f"User {user_id} not connected.")

    async def broadcast(self, message: dict):
        for user_id, websocket in self.active_connections.items():
            try:
                await websocket.send_json(message)
                logging.info(f"Broadcast message sent to {user_id}: {message}")
            except Exception as e:
                logging.error(f"Error sending message to {user_id}: {e}")


manager = ConnectionManager()


@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    # Ambil parameter `user_id` dari query string
    user_id = websocket.query_params.get("user_id")
    if not user_id:
        await websocket.close(code=1008)  # Tutup jika `user_id` tidak diberikan
        logging.error("WebSocket connection closed: Missing 'user_id'")
        return

    logging.info(f"WebSocket connection initiated with user_id: {user_id}")
    await manager.connect(websocket, user_id)

    try:
        while True:
            await websocket.receive_text()  # Menerima pesan dari client (misalnya ping/pong)
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        logging.info(f"WebSocket disconnected for user_id: {user_id}")


async def broadcast_notification(notification: dict, user_id: str):
    """
    Kirim notifikasi ke user tertentu berdasarkan user_id.
    """
    if user_id in manager.active_connections:
        await manager.send_personal_message(notification, user_id)
    else:
        logging.warning(
            f"User {user_id} not connected. Active connections: {list(manager.active_connections.keys())}"
        )


async def broadcast_length_notification(notification: dict, user_id: str):
    """
    Kirim notifikasi ke user tertentu berdasarkan user_id.
    """
    if user_id in manager.active_connections:
        await manager.send_personal_message(notification, user_id)
    else:
        logging.warning(
            f"User {user_id} not connected. Active connections: {list(manager.active_connections.keys())}"
        )
