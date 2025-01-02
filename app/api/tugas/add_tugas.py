from fastapi import Depends,HTTPException,Response
import sqlalchemy as sa
from pydantic import BaseModel, model_validator
import datetime
from app.dependencies.autentication import Autentication

from app.models.tugas import Tugas
from app.models.user import User
from app.dependencies.get_db_session import get_db_session
from app.dependencies.str_to_date import str_to_date

class AddTugasData(BaseModel):
    judul:str
    deskripsi :str
    kpi: str
    start_date : str
    deadline: str
    id_divisi : int
    id_renker: int
    id_karyawan: str

async def tugas_add(data:AddTugasData,payload=Depends(Autentication()),session=Depends(get_db_session)):
    # cek nik tersedia
    karyawan_exis = session.execute(
        sa.select(User.id_karyawan).where(User.id_karyawan == data.id_karyawan)
        ).scalar()

    if not karyawan_exis :
        raise HTTPException(
            400, detail='karyawan tidak terdaftar')
    
    # cek nik tersedia
    judul_exis = session.execute(
        sa.select(Tugas.judul).where(Tugas.judul == data.judul)
        ).scalar()

    if judul_exis :
        raise HTTPException(
            400, detail='judul sudah terdaftar')

    id_user = payload.get('uid',0)
    access_user = session.execute(sa.select(User.access, User.divisi).where(User.id_karyawan == id_user)).fetchone()
    if access_user.access == 2 and access_user.divisi == data.id_divisi  :
        tugas = Tugas(
            judul = data.judul,
            deskripsi = data.deskripsi,
            kpi = data.kpi,
            start_date = str_to_date(data.start_date),
            deadline = str_to_date(data.deadline),
            id_divisi = data.id_divisi,
            id_renker = data.id_renker,
            id_karyawan = data.id_karyawan
        )
    elif access_user.access > 2:
        tugas = Tugas(
            judul = data.judul,
            deskripsi = data.deskripsi,
            kpi = data.kpi,
            start_date = str_to_date(data.start_date),
            deadline = str_to_date(data.deadline),
            id_divisi = data.id_divisi,
            id_renker = data.id_renker,
            id_karyawan = data.id_karyawan,
            status = 2
        )
    else :
        raise HTTPException(
            400, detail='maaf anda tidak memiliki access')

    session.add(tugas)
    session.commit()

    return