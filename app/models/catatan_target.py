import datetime
import sqlalchemy as sa
from app.models import Base
from sqlalchemy.orm import relationship

class CatatanTarget(Base):
    __tablename__ = 'catatan_target'
    id_catatan = sa.Column('id_catatan', sa.Integer, primary_key=True, autoincrement=True)
    id_target = sa.Column('id_target', sa.Integer, sa.ForeignKey('target.id_target'), nullable=False)
    catatan = sa.Column('catatan', sa.String(500), nullable=False)
    created_at = sa.Column('created_at', sa.DateTime(timezone=True), default=datetime.datetime.now)
    modified_at = sa.Column('modified_at', sa.DateTime(timezone=True), default=datetime.datetime.now, onupdate=datetime.datetime.now)

# Relasi Many-to-One: Catatan Target-> Target
    target = relationship("Target", back_populates="catatan_target")
