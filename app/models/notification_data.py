import datetime
import sqlalchemy as sa
from sqlalchemy.types import Enum
from app.models import Base
from sqlalchemy.orm import relationship


class NotificationData(Base):
    __tablename__ = 'notification_data'
    id_notification_data = sa.Column('id_notification_data', sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column('title', sa.String(255), nullable=False)
    body = sa.Column('body', sa.String(500), nullable=False)
    id_karyawan = sa.Column('id_karyawan', sa.String(10), nullable=True)
    id_divisi = sa.Column('id_divisi', sa.Integer, nullable=True)
    access_level_user = sa.Column('access_level_user', sa.Integer, nullable=True)
    created_by = sa.Column('created_by', sa.String(100), nullable=True)
    link = sa.Column('link', sa.String(500), nullable=True)
    created_at = sa.Column('created_at', sa.DateTime, default=datetime.datetime.now, nullable=False)
    modified_at = sa.Column('modified_at', sa.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    user_notification = relationship("UserNotification", back_populates="notification_data")