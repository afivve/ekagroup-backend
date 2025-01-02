from fastapi import Depends, HTTPException
import sqlalchemy as sa
from pydantic import BaseModel

from app.models.push_notification import PushNotification
from app.models.user_notification import UserNotification
from app.dependencies.get_db_session import get_db_session

UserNotification


class AddNotificationData(BaseModel):
    id_karyawan: str
    token: str
    status: bool = False

async def check_token(id_karyawan: str, session=Depends(get_db_session)):
    # Cek apakah ada token yang terdaftar untuk id_karyawan
    token_exists = session.execute(
        sa.select(PushNotification.token)
        .where(PushNotification.id_karyawan == id_karyawan)
    ).scalar()

    if token_exists:
        return {"exists": True}
    else:
        return {"exists": False}

async def add_notification(data: AddNotificationData, session=Depends(get_db_session)):
    # Cek apakah `id_karyawan` sudah ada di tabel user
    id_karyawan_exists = session.execute(
        sa.text("SELECT id_karyawan FROM user WHERE id_karyawan = :id_karyawan"),
        {"id_karyawan": data.id_karyawan},
    ).scalar()

    if not id_karyawan_exists:
        raise HTTPException(
            status_code=404, detail="ID karyawan tidak ditemukan"
        )

    # Hapus semua notifikasi lama dengan `id_karyawan` yang sama
    session.execute(
        sa.delete(PushNotification).where(PushNotification.id_karyawan == data.id_karyawan)
    )

    # Tambahkan data notifikasi baru
    notification = PushNotification(
        id_karyawan=data.id_karyawan,
        token=data.token,
        status=data.status,
    )

    session.add(notification)
    session.commit()

    return {"message": "Notifikasi berhasil ditambahkan dan data lama dihapus."}
