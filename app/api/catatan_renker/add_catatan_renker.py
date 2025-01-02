from fastapi import Depends, HTTPException, status, Response
import sqlalchemy as sa
from pydantic import BaseModel, model_validator
import datetime
import logging
from app.dependencies.autentication import Autentication

from app.models.catatan_renker import CatatanRenker
from app.models.user import User
from app.dependencies.get_db_session import get_db_session
from app.dependencies.str_to_date import str_to_date
from app.utils.create_notification import create_notification_payload, save_notification
from app.api.notification.websocket_notification import broadcast_notification

from fastapi.responses import JSONResponse

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class AddCatatanRenkerData(BaseModel):
    id_renker: int
    catatan: str


async def add_catatan_renker(
    data: AddCatatanRenkerData,
    payload=Depends(Autentication()),
    session=Depends(get_db_session),
):
    """
    Add a new catatan renker and send a notification.
    """
    try:

        logger.info("Payload content: %s", payload)

        logger.info("Adding a new catatan renker...")

        # Create a new catatan renker entry
        catatan_renker = CatatanRenker(
            id_renker=data.id_renker,
            catatan=data.catatan,
        )

        session.add(catatan_renker)
        session.commit()
        logger.info(
            "Catatan renker added successfully with ID %s", catatan_renker.id_catatan
        )

        # Create notification payload
        catatan_body = data.catatan[:20]
        if len(data.catatan) > 20:
            catatan_body += "..."

        notification_payload = create_notification_payload(
            title="Membuat Rencana Kerja Baru",
            body=catatan_body,
            created_by=payload.get("username", "Unknown User"),
            link=f"rencana_kerja/{data.id_renker}",
            id_karyawan=payload.get("uid", "Unknown Divisi"),
            id_divisi=payload.get("divisi_id", "Unknown Divisi"),
            access_level_user=None,
        )

        notification = {
            "title": "Membuat Rencana Kerja Baru",
            "body": catatan_body,
            "created_by": payload.get("username", "Unknown User"),
            "link": f"rencana_kerja/{data.id_renker}",
            "id_karyawan": payload.get("uid", "Unknown Divisi"),
            "id_divisi": payload.get("divisi_id", "Unknown Divisi"),
            "access_level_user": None,
        }

        id_karyawan = payload.get("uid")

        # await broadcast_notification(user_id=id_karyawan, notification=notification)

        # Save notification
        # await save_notification(notification_payload, session)

        return {"success": True, "message": "Catatan Renker added successfully."}
    except Exception as e:
        print(f"Error occurred: {str(e)}")

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Internal server error",
                "code": 500,
            },
        )
