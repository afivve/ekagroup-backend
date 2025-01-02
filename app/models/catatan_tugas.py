import datetime
import sqlalchemy as sa
from app.models import Base
from sqlalchemy.orm import relationship

class CatatanTugas(Base):
    __tablename__ = 'catatan_tugas'
    id_catatan = sa.Column('id_catatan', sa.Integer, primary_key=True, autoincrement=True)
    id_tugas = sa.Column('id_tugas', sa.Integer, sa.ForeignKey('tugas.id_tugas'), nullable=False)
    catatan = sa.Column('catatan', sa.String(500), nullable=False)
    created_at = sa.Column('created_at', sa.DateTime(timezone=True), default=datetime.datetime.now)
    modified_at = sa.Column('modified_at', sa.DateTime(timezone=True), default=datetime.datetime.now, onupdate=datetime.datetime.now)

# Relasi Many-to-One: Catatan Target-> Target
    tugas = relationship("Tugas", back_populates="catatan_tugas")