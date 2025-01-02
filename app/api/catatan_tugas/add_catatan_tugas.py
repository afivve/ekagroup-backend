# from fastapi import Depends, HTTPException
# import sqlalchemy as sa
# from pydantic import BaseModel
# from app.dependencies.autentication import Autentication
# from app.models.catatan_tugas import CatatanTugas
# from app.models.user import User
# from app.dependencies.get_db_session import get_db_session
# from app.utils.create_notification import send_notification
# import logging

# #
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)


# STATIC_TOKEN = "dkBgPKsu_KkSOMFhnJmaEb:APA91bFaKacD7xRUiqxM1QgIAxBdZP5u-1nhg0dOYSYzCCFf8boVouLYfr16PKhO1LIY1BosLngaBkM2FkKdlap4gYg715iZz_AfoerSoG-vKdHDJ5GmAXA"

# class AddCatatanTugasData(BaseModel):
#     id_tugas: int
#     catatan: str

# async def add_catatan_tugas(data: AddCatatanTugasData, payload=Depends(Autentication()), session=Depends(get_db_session)):

#     catatan_tugas = CatatanTugas(
#         id_tugas=data.id_tugas,
#         catatan=data.catatan,
#     )
#     session.add(catatan_tugas)

#     try:

#         user_id = payload.get("id_karyawan")
#         user = session.query(User).filter(User.id_karyawan == user_id).first()

#         if user:
#             user.token = STATIC_TOKEN
#             session.add(user)
#             logger.info(f"Token disimpan untuk pengguna ID {user_id}.")
#         else:
#             logger.warning(f"Pengguna dengan ID {user_id} tidak ditemukan.")


#         try:
#             notification_response = await send_notification(
#                 token=STATIC_TOKEN,
#                 title="Catatan Baru Ditambahkan",
#                 body=f"Catatan baru telah ditambahkan untuk tugas ID {data.id_tugas}.",
#             )
#             logger.info(f"Notifikasi berhasil dikirim: {notification_response}")
#         except Exception as notif_error:
#             logger.error(f"Gagal mengirim notifikasi: {notif_error}")
#             raise HTTPException(status_code=500, detail=f"Gagal mengirim notifikasi: {notif_error}")


#         session.commit()

#         return {
#             "message": "Catatan tugas berhasil ditambahkan.",
#             "notification": notification_response,
#         }

#     except Exception as e:
#         session.rollback()
#         logger.error(f"Terjadi kesalahan: {e}")
#         raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {e}")


# import asyncio
# from fastapi import Depends, HTTPException
# import sqlalchemy as sa
# from pydantic import BaseModel
# from app.dependencies.autentication import Autentication
# from app.models.catatan_tugas import CatatanTugas
# from app.dependencies.get_db_session import get_db_session
# from app.utils.push_notification import push_notification
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# STATIC_TOKEN = "dkBgPKsu_KkSOMFhnJmaEb:APA91bG0R1HobrxorOGW2dUcPc9VH8cyvzoR82WgfTLRInEVTchI7y5T34Wm7TQm2GBc0jzjwtHrknX4eSPAie5hzKsDoqIpEgZF8-5CGFSrxpQZbDiYQgU"

# class AddCatatanTugasData(BaseModel):
#     id_tugas: int
#     catatan: str

# async def add_catatan_tugas(data: AddCatatanTugasData, payload=Depends(Autentication()), session=Depends(get_db_session)):
#     catatan_tugas = CatatanTugas(
#         id_tugas=data.id_tugas,
#         catatan=data.catatan,
#     )
#     session.add(catatan_tugas)

#     try:
#         # Commit data ke database
#         session.commit()

#         # Tambahkan jeda waktu 4 detik
#         await asyncio.sleep(4)

#         try:
#             # Kirim notifikasi setelah jeda
#             notification_response = await push_notification(
#                 token=STATIC_TOKEN,
#                 title="Catatan Baru Ditambahkan",
#                 body=f"Catatan baru telah ditambahkan untuk tugas ID {data.id_tugas}.",
#             )
#             logger.info(f"Notifikasi berhasil dikirim: {notification_response}")
#         except Exception as notif_error:
#             logger.error(f"Gagal mengirim notifikasi: {notif_error}")
#             raise HTTPException(status_code=500, detail=f"Gagal mengirim notifikasi: {notif_error}")

#         return {
#             "message": "Catatan tugas berhasil ditambahkan.",
#             "notification": notification_response,
#         }

#     except Exception as e:
#         session.rollback()
#         logger.error(f"Terjadi kesalahan: {e}")
#         raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {e}")


from fastapi import Depends, HTTPException, Response, status
import sqlalchemy as sa
from pydantic import BaseModel
from app.dependencies.autentication import Autentication
from app.models.catatan_tugas import CatatanTugas
from app.models.push_notification import PushNotification
from app.models.user import User
from app.dependencies.get_db_session import get_db_session
from app.utils.create_notification import create_notification_payload, save_notification
from app.api.notification.websocket_notification import broadcast_notification
from app.utils.push_notification import push_notification
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AddCatatanTugasData(BaseModel):
    id_tugas: int
    catatan: str
    id_karyawan: str  # Tambahkan id_karyawan dari request frontend


async def add_catatan_tugas(
    data: AddCatatanTugasData,
    payload=Depends(Autentication()),
    session=Depends(get_db_session),
):
    try:
        # Buat entri baru untuk CatatanTugas
        catatan_tugas = CatatanTugas(
            id_tugas=data.id_tugas,
            catatan=data.catatan,
        )

        # Truncate catatan body jika lebih dari 20 karakter untuk preview notifikasi
        catatan_body = data.catatan[:30]
        if len(data.catatan) > 30:
            catatan_body += "..."

        # Simpan entri baru ke database
        session.add(catatan_tugas)
        session.commit()

        # Kirim push notification hanya ke id_karyawan yang diminta
        token_query = (
            session.query(PushNotification.token)
            .filter(PushNotification.id_karyawan == data.id_karyawan)
            .first()
        )

        created_by = payload.get("username")

        if token_query:
            token = token_query[0]
            notification_response = await push_notification(
                token=token,
                title=f"{created_by} : Menambahkan Catatan Tugas ",
                body=catatan_body,
            )
            logger.info(
                f"Notifikasi berhasil dikirim ke {data.id_karyawan} dengan token {token}: {notification_response}"
            )
        else:
            logger.warning(
                f"Tidak ditemukan token untuk id_karyawan: {data.id_karyawan}"
            )

        # Persiapkan payload untuk notifikasi
        notification_payload = create_notification_payload(
            title="Menambahkan Catatan Tugas",
            body=catatan_body,
            created_by=payload.get("username", "Unknown User"),
            link=f"tugas/{data.id_tugas}",
            id_karyawan=data.id_karyawan,  # Kirim hanya ke id_karyawan ini
        )

        id_kar = "A015"
        id_karyawan = data.id_karyawan
        # Kirim notifikasi melalui websocket
        await broadcast_notification(
            notification=notification_payload, user_id=id_karyawan
        )

        # Simpan notifikasi ke database
        await save_notification(notification_payload, session)

        return {"message": "Catatan Tugas added successfully!"}

    except HTTPException as e:
        # Tangani HTTP-specific exceptions (misalnya, data tidak ditemukan)
        raise e

    except Exception as e:
        # Tangani kesalahan umum
        session.rollback()  # Rollback jika ada error
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while adding the Catatan Tugas: {str(e)}",
        )
