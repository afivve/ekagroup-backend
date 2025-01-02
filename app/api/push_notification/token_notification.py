from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from pydantic import BaseModel
import sqlalchemy as sa

from app.dependencies.get_db_session import get_db_session
from app.dependencies.autentication import Autentication
from app.models.push_notification import PushNotification

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class AddPushNotificationRequest(BaseModel):
    token: str


async def save_firebase_token(
    request: AddPushNotificationRequest,
    session=Depends(get_db_session),
    payload=Depends(Autentication()),
):
    """
    Add or update a push notification token for a user based on their id_karyawan.
    """
    try:
        # Get id_karyawan from authentication payload
        id_karyawan = payload.get("uid")

        # Check if a token already exists for this user
        push_notification = session.execute(
            sa.select(PushNotification).where(
                PushNotification.id_karyawan == id_karyawan
            )
        ).scalar_one_or_none()

        if push_notification:
            # If the new token is the same as the existing token, do nothing
            if push_notification.token == request.token:
                return {"message": "Token is already up to date."}
            else:
                # Update the existing token
                push_notification.token = request.token
                session.commit()
                return {"message": "Push notification token updated successfully."}
        else:
            # Add a new token if none exists
            new_push_notification = PushNotification(
                id_karyawan=id_karyawan,
                token=request.token,
            )
            session.add(new_push_notification)
            session.commit()
            return {"message": "Push notification token added successfully."}

    except HTTPException as e:
        # Handle HTTP-specific exceptions
        logger.error(f"HTTP error while updating push notification: {str(e)}")
        raise e

    except Exception as e:
        # Handle general exceptions
        session.rollback()  # Rollback any changes in case of error
        logger.error(f"Error while updating push notification: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
