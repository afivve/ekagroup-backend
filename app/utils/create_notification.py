import datetime
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notification_data import NotificationData
from app.models.unread_notification import UnreadNotificationUser
from app.models.user_notification import UserNotification
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.dependencies.get_db_session import get_db_session
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from app.api.notification.websocket_notification import broadcast_length_notification


logger = logging.getLogger(__name__)


def create_notification_payload(
    title: str,
    body: str,
    created_by: str,
    link: str = None,
    id_karyawan: str = None,
):
    """
    Helper function to create a notification payload.
    """
    return {
        "title": title,
        "body": body,
        "created_by": created_by,
        "link": link,
        "id_karyawan": id_karyawan,
    }


from sqlalchemy.future import select
from sqlalchemy.orm import Session
import datetime


async def save_notification(
    notification_payload: dict, session=Depends(get_db_session)
):
    """
    Save a notification to the database and update unread notifications count in UnreadNotificationUser.

    Args:
        notification_payload (dict): A dictionary containing the notification data.
        session (Session): The SQLAlchemy session.

    Returns:
        NotificationData: The created NotificationData instance.
    """
    try:
        # Create the new notification
        new_notification = NotificationData(
            title=notification_payload["title"],
            body=notification_payload["body"],
            created_by=notification_payload["created_by"],
            link=notification_payload.get("link"),
            id_karyawan=notification_payload.get("id_karyawan"),
        )

        # Add the notification to the session and commit
        session.add(new_notification)
        session.commit()

        # Get id_karyawan from the payload
        id_karyawan = notification_payload.get("id_karyawan")

        # Query to get all notification IDs that the user has already read
        read_query = select(UserNotification.id_notification_data).filter(
            UserNotification.id_karyawan == id_karyawan
        )
        read_result = session.execute(read_query)
        read_notifications = set(
            read_result.scalars().all()
        )  # Convert to set for faster lookup

        # Query to get the count of notifications that the user has not read
        unread_query = select(NotificationData.id_notification_data).filter(
            NotificationData.id_karyawan == id_karyawan,
            NotificationData.id_notification_data.notin_(read_notifications),
        )
        unread_result = session.execute(unread_query)
        unread_count = len(
            unread_result.scalars().all()
        )  # Get the count of unread notifications

        # Query the UnreadNotificationUser to find the user's unread count
        unread_query = select(UnreadNotificationUser).filter(
            UnreadNotificationUser.id_karyawan == id_karyawan
        )
        unread_result = session.execute(unread_query)
        unread_record = unread_result.scalars().first()

        # If unread record exists, increment the total_unread by 1
        if unread_record:
            unread_record.total_unread = (
                unread_count  # Update with the new unread count
            )
            unread_record.modified_at = (
                datetime.datetime.now()
            )  # Update the modified timestamp
        else:
            # If the record does not exist, create a new one with the unread count
            new_unread_record = UnreadNotificationUser(
                id_karyawan=id_karyawan,
                total_unread=unread_count,
            )
            session.add(new_unread_record)

        notification_length = {
            "unread_count": unread_count,
            "success": True,
            "message": "Unread notifications count fetched successfully",
            "code": 200,
        }

        id_kar = "A015"

        await broadcast_length_notification(
            notification=notification_length, user_id=id_karyawan
        )

        session.commit()

        return new_notification

    except SQLAlchemyError as e:
        logger.error(f"Failed to save notification: {e}")
        session.rollback()
        raise


# async def save_notification(notification_payload: dict, session=Depends(get_db_session)):
#     """
#     Save a notification to the database.

#     Args:
#         notification_payload (dict): A dictionary containing the notification data.
#         db_session (AsyncSession): The SQLAlchemy async session.

#     Returns:
#         NotificationData: The created NotificationData instance.
#     """
#     try:
#         new_notification = NotificationData(
#             title=notification_payload["title"],
#             body=notification_payload["body"],
#             created_by=notification_payload["created_by"],
#             link=notification_payload.get("link"),
#             id_karyawan=notification_payload.get("id_karyawan"),
#             id_divisi=notification_payload.get("id_divisi"),
#             access_level_user=notification_payload.get("access_level_user"),
#         )

#         session.add(new_notification)
#         session.commit()
#         return new_notification
#     except SQLAlchemyError as e:
#         logger.error(f"Failed to save notification: {e}")
#         session.rollback()
#         raise
