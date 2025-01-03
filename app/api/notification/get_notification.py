# from typing import List
# import logging
# from fastapi import APIRouter, Depends, HTTPException
# from fastapi.encoders import jsonable_encoder
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select

# from app.models.notification_data import NotificationData
# from app.dependencies.get_db_session import get_db_session
# from app.api_models import BaseResponseModel
# from app.api_models.notification_model import NotificationModel

# from pydantic import BaseModel

# from app.dependencies.autentication import Autentication


# # Logger setup
# logger = logging.getLogger(__name__)

# # Define response model for notifications
# class GetNotificationsResponseModel(BaseResponseModel):
#     data: List[NotificationModel]

#     class Config:
#         json_schema_extra = {
#             'example': {
#                 'data': [
#                     {
#                         "id": 1,
#                         "title": "New Work Plan",
#                         "body": "Here is the body of the notification...",
#                         "created_by": "Admin",
#                         "link": "http://example.com",
#                         "id_karyawan": "123",
#                         "id_divisi": 5,
#                         "access_level_user": 1
#                     }
#                 ],
#                 'jum': 10,
#                 'meta': {},
#                 'success': True,
#                 'message': 'Success',
#                 'code': 200
#             }
#         }

# class GetNotificationsData(BaseModel):
#     # Tidak perlu filter di sini untuk sekarang
#     pass

# # API Endpoint to get all notifications (without filters)
# async def get_notifications(
#     data: GetNotificationsData = Depends(),
#     session= Depends(get_db_session),
#     payload=Depends(Autentication())
# ):
#     logger.info("Fetching all notifications without filters.")

#     try:
#     # Get id_karyawan from payload
#         id_karyawan_payload = payload.get("uid")

#         # Ensure that id_karyawan is provided in the payload
#         if not id_karyawan_payload:
#             raise HTTPException(status_code=400, detail="Missing 'uid' in request payload")

#         # Query to get notifications filtered by id_karyawan
#         query = select(NotificationData).filter(NotificationData.id_karyawan == id_karyawan_payload)

#         # Execute the query
#         result = session.execute(query)
#         notifications = result.scalars().all()

#         # Log notifications to check for None values
#         logger.info(f"Fetched notifications: {notifications}")

#         # Check if any notifications are None and raise an error
#         if any(notification is None for notification in notifications):
#             raise HTTPException(status_code=500, detail="Some notifications are missing data")

#         # Log the number of notifications fetched
#         logger.info("Successfully fetched %d notifications", len(notifications))

#         # Convert to response model, skipping any None values
#         data_list = [
#             NotificationModel(
#                 id_notification_data=notification.id_notification_data,
#                 title=notification.title,
#                 body=notification.body,
#                 created_by=notification.created_by,
#                 link=notification.link,
#                 id_karyawan=notification.id_karyawan,
#                 id_divisi=notification.id_divisi,
#                 access_level_user=notification.access_level_user
#             )
#             for notification in notifications if notification is not None
#         ]

#         # Return the response model
#         return GetNotificationsResponseModel(data=data_list)

#     except Exception as e:
#         logger.error(f"Error fetching notifications: {e}")
#         raise HTTPException(status_code=500, detail="Internal server error")

from typing import List
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.notification_data import NotificationData
from app.models.user_notification import UserNotification
from app.models.user import User
from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel
from app.api_models.notification_model import NotificationModel
from app.models.unread_notification import UnreadNotificationUser
from app.dependencies.autentication import Autentication
from pydantic import BaseModel
from app.api.notification.websocket_notification import broadcast_notification

from datetime import datetime
import pytz
from sqlalchemy import or_


def calculate_relative_time(created_at: datetime) -> str:
    """
    Menghitung waktu relatif dari `created_at` hingga saat ini dalam zona waktu Indonesia.
    """
    # Konversi waktu ke zona waktu Indonesia (WIB)
    indo_tz = pytz.timezone("Asia/Jakarta")
    created_at_local = created_at.astimezone(indo_tz)
    now_local = datetime.now(indo_tz)

    delta = now_local - created_at_local

    if delta.days > 0:
        if delta.days == 1:
            return "1 hari lalu"
        return f"{delta.days} hari lalu"

    hours = delta.seconds // 3600
    if hours > 0:
        if hours == 1:
            return "1 jam lalu"
        return f"{hours} jam lalu"

    minutes = delta.seconds // 60
    if minutes > 0:
        if minutes == 1:
            return "1 menit lalu"
        return f"{minutes} menit lalu"

    return "Baru saja"


# Logger setup
logger = logging.getLogger(__name__)


# Define response model for notifications
class GetNotificationsResponseModel(BaseResponseModel):
    data: List[NotificationModel]

    class Config:
        json_schema_extra = {
            "example": {
                "data": [
                    {
                        "id": 1,
                        "title": "New Work Plan",
                        "body": "Here is the body of the notification...",
                        "created_by": "Admin",
                        "link": "http://example.com",
                        "id_karyawan": "123",
                        "id_divisi": 5,
                        "access_level_user": 1,
                        "isRead": True,
                    }
                ],
                "jum": 10,
                "meta": {},
                "success": True,
                "message": "Success",
                "code": 200,
            }
        }


class GetNotificationsData(BaseModel):
    pass


# API Endpoint to get all notifications (without filters)
async def get_notifications(
    data: GetNotificationsData = Depends(),
    session: AsyncSession = Depends(get_db_session),
    payload=Depends(Autentication()),
):
    logger.info("Fetching all notifications without filters.")

    try:
        # Get id_karyawan from payload
        id_karyawan_payload = payload.get("uid")

        if not id_karyawan_payload:
            raise HTTPException(
                status_code=400, detail="Missing 'uid' in request payload"
            )

        # Ambil data user berdasarkan id_karyawan dari payload
        user = session.execute(
            select(User).filter(User.id_karyawan == id_karyawan_payload)
        ).scalar_one_or_none()

        # if not user:
        #     raise HTTPException(status_code=404, detail="User not found")

        # Query notifikasi dengan filter tambahan berdasarkan divis_id dan access_level
        query = (
            select(NotificationData)
            .filter(
                NotificationData.id_karyawan == id_karyawan_payload,
            )
            .order_by(NotificationData.created_at.desc())
        )
        result = session.execute(query)
        notifications = result.scalars().all()

        # Query to check which notifications have been read
        read_query = select(UserNotification.id_notification_data).filter(
            UserNotification.id_karyawan == id_karyawan_payload
        )
        read_result = session.execute(read_query)
        read_notifications = set(
            read_result.scalars().all()
        )  # Convert to set for faster lookup

        # Map notifications to response model
        data_list = [
            NotificationModel(
                id_notification_data=notification.id_notification_data,
                title=notification.title,
                body=notification.body,
                created_by=notification.created_by,
                link=notification.link,
                id_karyawan=notification.id_karyawan,
                id_divisi=notification.id_divisi,
                access_level_user=notification.access_level_user,
                isRead=notification.id_notification_data in read_notifications,
                relative_time=calculate_relative_time(notification.created_at),
            )
            for notification in notifications
        ]

        return GetNotificationsResponseModel(
            data=data_list, success=True, message="Success", code=200
        )

    except Exception as e:
        logger.error(f"Error fetching notifications: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


class UnreadNotificationsCountResponse(BaseModel):
    unread_count: int
    success: bool
    message: str
    code: int

    class Config:
        json_schema_extra = {
            "example": {
                "unread_count": 5,
                "success": True,
                "message": "Unread notifications count fetched successfully",
                "code": 200,
            }
        }


# Function to get the count of unread notifications for a specific user
async def get_unread_notifications_count(
    session=Depends(get_db_session), payload=Depends(Autentication())
) -> UnreadNotificationsCountResponse:
    logger.info("Fetching unread notifications count.")

    try:
        # Get id_karyawan from payload
        id_karyawan_payload = payload.get("uid")

        if not id_karyawan_payload:
            raise HTTPException(
                status_code=400, detail="Missing 'uid' in request payload"
            )

        # Query to get the unread count from the UnreadNotificationUser model
        unread_query = select(UnreadNotificationUser).filter(
            UnreadNotificationUser.id_karyawan == id_karyawan_payload
        )
        unread_result = session.execute(unread_query)
        unread_record = unread_result.scalars().first()

        if unread_record:
            unread_count = (
                unread_record.total_unread
            )  # Get the unread count from the model
        else:
            unread_count = (
                0  # If no record exists, assume there are no unread notifications
            )

        notification = {
            "unread_count": unread_count,
            "success": True,
            "message": "Unread notifications count fetched successfully",
            "code": 200,
        }

        id_kar = "A015"

        # Optionally broadcast the count (if needed in the WebSocket logic)
        await broadcast_notification(
            notification=notification, user_id=id_karyawan_payload
        )

        return UnreadNotificationsCountResponse(
            unread_count=unread_count,
            success=True,
            message="Unread notifications count fetched successfully",
            code=200,
        )

    except Exception as e:
        logger.error(f"Error fetching unread notifications count: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
