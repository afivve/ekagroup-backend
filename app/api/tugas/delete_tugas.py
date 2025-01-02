from typing import Optional
from fastapi import Depends,HTTPException,Response
import sqlalchemy as sa
from pydantic import BaseModel
from app.dependencies.autentication import Autentication

from app.models.tugas import Tugas
from app.dependencies.get_db_session import get_db_session

from app.models.user import User

class DeleteTugasData(BaseModel):
    id_tugas: int  = None
    id_divisi :str

async def delete_tugas(data:DeleteTugasData,payload=Depends(Autentication()),session=Depends(get_db_session)):

    # cek akses
    id_strong_user = payload.get('uid', 0)

    user_access = session.execute(sa.select(User.access,User.id_karyawan).where(User.id_karyawan == id_strong_user)).scalar()
    print("Uacc",user_access) 
    if user_access < 3 or user_access.id_divisi != data.id_divisi:
        raise HTTPException(400, detail='anda tidak memiliki akses')

    # cek id tersedia
    id_exis = session.execute(
        sa.select(Tugas.id_tugas).where(Tugas.id_tugas == data.id_tugas)
        ).scalar()

    if not id_exis :
        raise HTTPException(
            400, detail='target yang dimaksud tidak tersedia')


    result = session.execute(
        sa.delete(Tugas).where(Tugas.id_tugas == data.id_tugas)
    )
    if result.rowcount == 0:
        raise HTTPException(400, detail='tugasa not found')


    session.commit()

    return