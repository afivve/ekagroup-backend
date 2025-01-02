import datetime
import sqlalchemy as sa
from sqlalchemy.types import Enum
from app.models import Base

class UserLogin(Base):
    __tablename__ = 'user_login'
    id = sa.Column('id', sa.Integer, primary_key=True, autoincrement=True)
    id_karyawan = sa.Column('id_karyawan', sa.String(10), sa.ForeignKey('user.id_karyawan'), nullable=False)
    refresh_token = sa.Column('refresh_token', sa.String(500), nullable=False)
    expired_at = sa.Column('expired_at', sa.DateTime, nullable=False)
    created_at = sa.Column('created_at', sa.DateTime(timezone=True), default=datetime.datetime.now)
    modified_at = sa.Column('modified_at', sa.DateTime(timezone=True), default=datetime.datetime.now, onupdate=datetime.datetime.now)
    user_number = sa.Column('user_number', sa.Integer, nullable=True)
