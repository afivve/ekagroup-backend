import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user_notification import UserNotification
from app.models.notification_data import NotificationData
from app.dependencies.get_db_session import get_db_session
from app.dependencies.autentication import Autentication
from app.models.unread_notification import UnreadNotificationUser
from app.api.notification.websocket_notification import broadcast_length_notification

from pydantic import BaseModel

# Logger setup
import logging

logger = logging.getLogger(__name__)

# API Router Setup
router = APIRouter()


# Pydantic model to handle input for POST request
class MarkNotificationReadRequest(BaseModel):
    id_notification_data: int  # ID of the notification
    id_karyawan: str  # Employee ID of the user


# Fungsi POST untuk menambahkan notifikasi yang dibaca
async def mark_notification_read(
    id_notification_data: int,
    session=Depends(get_db_session),
    payload=Depends(Autentication()),  # Authentication dependency to ensure valid user
):
    try:
        # Query to check if the notification exists

        id_karyawan = payload.get("uid", "Tidak ada uid")

        query = select(NotificationData).filter(
            NotificationData.id_notification_data == id_notification_data
        )
        result = session.execute(query)
        notification = result.scalars().first()

        # if not notification:
        #     raise HTTPException(status_code=404, detail="Notification not found")

        # Check if the notification has already been marked as read by this user
        check_existing_query = select(UserNotification).filter(
            UserNotification.id_karyawan == id_karyawan,
            UserNotification.id_notification_data == id_notification_data,
        )
        result = session.execute(check_existing_query)
        existing_entry = result.scalars().first()

        if existing_entry:
            # If notification already marked as read, just return a success message
            return {"message": "Notification already marked as read"}

        # Create a new UserNotification record to mark the notification as read
        user_notification = UserNotification(
            id_karyawan=id_karyawan, id_notification_data=id_notification_data
        )
        session.add(user_notification)

        # Update UnreadNotificationUser to decrease unread count by 1
        unread_query = select(UnreadNotificationUser).filter(
            UnreadNotificationUser.id_karyawan == id_karyawan
        )
        unread_result = session.execute(unread_query)
        unread_record = unread_result.scalars().first()

        if unread_record:
            # If the unread record exists, decrease the total_unread by 1
            unread_record.total_unread = max(
                unread_record.total_unread - 1, 0
            )  # Prevent negative unread count
            unread_record.modified_at = (
                datetime.datetime.now()
            )  # Update the modified timestamp
        else:
            # If no unread record exists, create one with total_unread = 0 (since it's already read)
            new_unread_record = UnreadNotificationUser(
                id_karyawan=id_karyawan,
                total_unread=0,
            )
            session.add(new_unread_record)

        # Commit the transaction
        session.commit()

        # Prepare the notification length for broadcasting (return only serializable fields)
        notification_length = {
            "unread_count": unread_record.total_unread if unread_record else 0,
            "success": True,
            "message": "Unread notifications count fetched successfully",
            "code": 200,
        }

        id_kar = "A015"

        await broadcast_length_notification(
            notification=notification_length, user_id=id_karyawan
        )

        return {"message": "Notification marked as read successfully."}

    except Exception as e:
        logger.error(f"Error marking notification as read: {e}")
        session.rollback()  # Ensure we rollback if any error happens
        raise HTTPException(status_code=500, detail="Internal server error")
