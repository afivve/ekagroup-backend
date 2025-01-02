import datetime
import sqlalchemy as sa
from sqlalchemy.types import Enum
from app.models import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id_karyawan = sa.Column("id_karyawan", sa.String(10), primary_key=True)
    username = sa.Column("username", sa.String(256), nullable=True, unique=True)
    password = sa.Column("password", sa.String(512), nullable=True)
    full_name = sa.Column("full_name", sa.String(256), nullable=True)
    email = sa.Column("email", sa.String(100), nullable=True)
    alamat = sa.Column("alamat", sa.String(500), nullable=True)
    noWa = sa.Column("noWa", sa.String(16), nullable=True)
    access = sa.Column("access", sa.Integer(), default=0)
    path_foto = sa.Column("path_foto", sa.String(255), nullable=True)
    divisi_id = sa.Column(
        "divisi", sa.Integer, sa.ForeignKey("divisi.id_divisi"), nullable=True
    )
    jabatan = sa.Column("jabatan", sa.String(100), nullable=True)
    jenis_kelamin = sa.Column("jenis_kelamin", sa.String(16), nullable=True)
    tgl_lahir = sa.Column("tgl_lahir", sa.DateTime, nullable=True)
    nik = sa.Column("nik", sa.String(16), default=False)
    created_at = sa.Column(
        "created_at", sa.DateTime(timezone=True), default=datetime.datetime.now
    )
    modified_at = sa.Column(
        "modified_at",
        sa.DateTime(timezone=True),
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
    )

    # Relasi User -> Divisi
    divisi = relationship("Divisi", back_populates="user")

    # Relasi User -> Tugas
    tugas = relationship("Tugas", back_populates="user")

    user_notification = relationship("UserNotification", back_populates="user")

    unread_notification_user = relationship(
        "UnreadNotificationUser", back_populates="user"
    )

    push_notification = relationship("PushNotification", back_populates="user")
