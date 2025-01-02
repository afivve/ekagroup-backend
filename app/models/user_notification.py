import datetime
import sqlalchemy as sa
from sqlalchemy.types import Enum
from app.models import Base
from sqlalchemy.orm import relationship


class UserNotification(Base):
    __tablename__ = 'user_notification'
    id_user_notification = sa.Column('id_user_notification', sa.Integer, primary_key=True, autoincrement=True)
    id_karyawan = sa.Column('id_karyawan', sa.String(10), sa.ForeignKey('user.id_karyawan'), nullable=True)
    id_notification_data = sa.Column('id_notifikasi_data', sa.Integer, sa.ForeignKey('notification_data.id_notification_data'), nullable=True)
    created_at = sa.Column('created_at', sa.DateTime, default=datetime.datetime.now, nullable=False)
    modified_at = sa.Column('modified_at', sa.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    notification_data = relationship("NotificationData", back_populates="user_notification")
    user = relationship("User", back_populates="user_notification")