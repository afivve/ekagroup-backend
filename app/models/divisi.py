import datetime
import sqlalchemy as sa
from app.models import Base
from sqlalchemy.orm import relationship


class Divisi(Base):
    __tablename__ = "divisi"

    id_divisi = sa.Column("id_divisi", sa.Integer, primary_key=True, autoincrement=True)
    nama_divisi = sa.Column("nama_divisi", sa.String(255), nullable=False, unique=True)
    path_foto = sa.Column("path_foto", sa.String(255), nullable=True)
    created_at = sa.Column(
        "created_at", sa.DateTime(timezone=True), default=datetime.datetime.now
    )
    modified_at = sa.Column(
        "modified_at",
        sa.DateTime(timezone=True),
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
    )

    # Relasi One-to-Many: Divisi -> User
    user = relationship("User", back_populates="divisi")

    # Relasi One-to-Many: Divisi -> Other Tables (e.g., Target, RencanaKerja, Tugas)
    target = relationship("Target", back_populates="divisi")
    rencana_kerja = relationship("RencanaKerja", back_populates="divisi")
    tugas = relationship("Tugas", back_populates="divisi")
    # notification_data = relationship("NotificationData", back_populates="divisi")
