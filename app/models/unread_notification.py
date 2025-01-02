import datetime
import sqlalchemy as sa
from sqlalchemy.types import Enum
from app.models import Base
from sqlalchemy.orm import relationship


class UnreadNotificationUser(Base):
    __tablename__ = 'unread_notification_user'
    id_unread_notification_user = sa.Column('id_unread_notification_user', sa.Integer, primary_key=True, autoincrement=True)
    total_unread = sa.Column('total_unread', sa.Integer)
    id_karyawan = sa.Column('id_karyawan', sa.String(10), sa.ForeignKey('user.id_karyawan'), nullable=True)
    created_at = sa.Column('created_at', sa.DateTime, default=datetime.datetime.now, nullable=False)
    modified_at = sa.Column('modified_at', sa.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    user = relationship("User", back_populates="unread_notification_user")