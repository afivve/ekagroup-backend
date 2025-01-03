import datetime
import sqlalchemy as sa
from sqlalchemy.types import Enum
from app.models import Base
from sqlalchemy.orm import relationship


class Target(Base):
    __tablename__ = "target"
    id_target = sa.Column("id_target", sa.Integer, primary_key=True, autoincrement=True)
    judul = sa.Column("judul", sa.String(255), nullable=False, unique=True)
    kpi = sa.Column("kpi", sa.String(255), nullable=True)
    deskripsi = sa.Column("deskripsi", sa.String(500), nullable=True)
    start_date = sa.Column("start_date", sa.DateTime, nullable=False)
    deadline = sa.Column("deadline", sa.DateTime, nullable=False)
    catatan = sa.Column("catatan", sa.String(500), nullable=True)
    file_name = sa.Column("file_name", sa.String(255), nullable=True)
    id_divisi = sa.Column(
        "id_divisi", sa.Integer, sa.ForeignKey("divisi.id_divisi"), nullable=False
    )
    status = sa.Column("status", sa.Integer, default=0, nullable=False)
    progres = sa.Column("progres", sa.Integer, default=0, nullable=False)
    prioritas = sa.Column("prioritas", sa.Integer, default=4, nullable=False)
    created_at = sa.Column(
        "created_at", sa.DateTime(timezone=True), default=datetime.datetime.now
    )
    modified_at = sa.Column(
        "modified_at",
        sa.DateTime(timezone=True),
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
    )

    # Relasi Many-to-One: Target -> Divisi
    divisi = relationship("Divisi", back_populates="target")

    # Relasi One-to-Many: Target -> Rencana Kerja
    rencana_kerja = relationship("RencanaKerja", back_populates="target")

    catatan_target = relationship("CatatanTarget", back_populates="target")
