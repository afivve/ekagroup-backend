import datetime
import sqlalchemy as sa
from sqlalchemy.types import Enum
from app.models import Base
from sqlalchemy.orm import relationship


class PushNotification(Base):
    __tablename__ = "push_notification"
    id = sa.Column(
        "id_push_notification", sa.Integer, primary_key=True, autoincrement=True
    )
    id_karyawan = sa.Column(
        "id_karyawan", sa.String(10), sa.ForeignKey("user.id_karyawan"), nullable=False
    )
    token = sa.Column("token", sa.TEXT)
    created_at = sa.Column(
        "created_at", sa.DateTime, default=datetime.datetime.now, nullable=False
    )
    modified_at = sa.Column(
        "modified_at",
        sa.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
    )

    user = relationship("User", back_populates="push_notification")
