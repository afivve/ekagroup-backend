import datetime
import sqlalchemy as sa
from app.models import Base
from sqlalchemy.orm import relationship

class CatatanRenker(Base):
    __tablename__ = 'catatan_renker'
    id_catatan = sa.Column('id_catatan', sa.Integer, primary_key=True, autoincrement=True)
    id_renker = sa.Column('id_renker', sa.Integer, sa.ForeignKey('rencana_kerja.id_renker'), nullable=False)
    catatan = sa.Column('catatan', sa.String(500), nullable=False)
    created_at = sa.Column('created_at', sa.DateTime(timezone=True), default=datetime.datetime.now)
    modified_at = sa.Column('modified_at', sa.DateTime(timezone=True), default=datetime.datetime.now, onupdate=datetime.datetime.now)

# Relasi Many-to-One: Catatam Rencana Kerja -> Rencana Kerja
    rencana_kerja = relationship("RencanaKerja", back_populates="catatan_renker")