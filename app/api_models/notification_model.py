from pydantic import BaseModel
from typing import Optional


class NotificationModel(BaseModel):
    id_notification_data: int
    title: str
    body: str
    created_by: Optional[str] = None
    link: Optional[str] = None
    id_karyawan: Optional[str] = None
    id_divisi: Optional[int] = None
    access_level_user: Optional[int] = None
    isRead: Optional[bool] = None
    relative_time: Optional[str] = None

    class Config:
        from_attributes = (
            True  # Allows Pydantic to read data even if it comes from SQLAlchemy models
        )
