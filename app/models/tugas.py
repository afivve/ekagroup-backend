import datetime
import sqlalchemy as sa
from sqlalchemy.types import Enum
from app.models import Base
from sqlalchemy.orm import relationship


class Tugas(Base):
    __tablename__ = "tugas"
    id_tugas = sa.Column("id_tugas", sa.Integer, primary_key=True, autoincrement=True)
    judul = sa.Column("judul", sa.String(255), nullable=False, unique=True)
    kpi = sa.Column("kpi", sa.String(255), nullable=True)
    deskripsi = sa.Column("deskripsi", sa.String(500), nullable=True)
    start_date = sa.Column("start_date", sa.DateTime, nullable=False)
    deadline = sa.Column("deadline", sa.DateTime, nullable=False)
    catatan = sa.Column("catatan", sa.String(500), nullable=True)
    file_name = sa.Column("file_name", sa.String(255), nullable=True)
    created_by = sa.Column("created_by", sa.String(255), nullable=True)
    id_karyawan = sa.Column(
        "id_karyawan", sa.String(10), sa.ForeignKey("user.id_karyawan"), nullable=False
    )
    id_renker = sa.Column(
        "id_renker", sa.Integer, sa.ForeignKey("rencana_kerja.id_renker"), nullable=True
    )
    id_divisi = sa.Column(
        "id_divisi", sa.Integer, sa.ForeignKey("divisi.id_divisi"), nullable=False
    )
    status = sa.Column("status", sa.Integer, nullable=False, default=1)
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

    # Relasi Many-to-One: Tugas -> User
    user = relationship("User", back_populates="tugas")

    # Relasi One-to-Many: Tugas -> Catatan Tugas
    catatan_tugas = relationship("CatatanTugas", back_populates="tugas")

    divisi = relationship("Divisi", back_populates="tugas")

    rencana_kerja = relationship("RencanaKerja", back_populates="tugas")
