from typing import Optional
from fastapi import Depends,HTTPException,Response
from fastapi.encoders import jsonable_encoder
import sqlalchemy as sa
from pydantic import BaseModel, model_validator
import datetime
from app.dependencies.autentication import Autentication

from app.models.target import Target
from app.dependencies.get_db_session import get_db_session
from app.dependencies.str_to_date import str_to_date

class UpdateTargettData(BaseModel):
    id_target:int = None
    judul:Optional[str] = None
    deskripsi :Optional[str] = None
    kpi: Optional[str] = None
    start_date : Optional[str] = None
    deadline: Optional[str] = None
    catatan : Optional[str] = None
    progres : Optional[int] = None
    status : Optional[int] = None
    file_name : Optional[str] = None




async def update_target(data:UpdateTargettData,payload=Depends(Autentication()),session=Depends(get_db_session)):
    id_exis = session.execute(
        sa.select(Target.id_target).where(Target.id_target == data.id_target)
        ).scalar()

    # cek id tersedia
    if not id_exis :
        raise HTTPException(
            400, detail='target yang dimaksud tidak tersedia')
    
    judul_exis = session.execute(
    sa.select(Target.judul).where(Target.judul == data.judul)
    ).scalar()

    # cek nik tersedia
    if judul_exis :
        raise HTTPException(
            400, detail='judul sudah terdaftar')

    target_data = jsonable_encoder(data)
    # TODO:
    values_to_update = {}

    if 'judul' in target_data and target_data['judul']:
        values_to_update.update({'judul': target_data['judul']})

    if 'deskripsi' in target_data and target_data['deskripsi']:
        values_to_update.update({'deskripsi': target_data['deskripsi']})

    if 'kpi' in target_data and target_data['kpi']:
        values_to_update.update({'kpi': target_data['kpi']})

    if 'start_date' in target_data and target_data['start_date']:
        values_to_update.update({'start_date': target_data['start_date']})

    if 'deadline' in target_data and target_data['deadline']:
        values_to_update.update({'deadline': target_data['deadline']})

    if 'catatan' in target_data and target_data['catatan']:
        values_to_update.update({'catatan': target_data['catatan']})

    if 'progres' in target_data and target_data['progres']:
        values_to_update.update({'progres': target_data['progres']})

    if 'status' in target_data and target_data['status']:
        values_to_update.update({'status': target_data['status']})

    if 'file_name' in target_data and target_data['file_name']:
        values_to_update.update({'file_name': target_data['file_name']})

    result = session.execute(
        sa.update(Target).values(**values_to_update).where(Target.id_target == data.id_target)
    )

    if result.rowcount == 0:
        raise HTTPException(400, detail='Target not found')


    session.commit()

    return