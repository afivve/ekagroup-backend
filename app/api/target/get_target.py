from typing import List, Optional

import jwt
import sqlalchemy as sa
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.api_models import BaseResponseModel
from app.api_models.target_model import TargetModel
from app.config import config
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.target import Target
from app.models.user import User


class GetTargetModel(BaseModel):
    id_target: int


class GetDataTargetResponseModel(BaseResponseModel):
    data: object

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "data": {
                        "id_target": 1,
                        "judul": "omset 200 jt per bulan",
                        "id_divisi": 2,
                        "deskripsi": "harus omset 200 jt per bulan",
                        "kpi": "ommset",
                        "deadline": 2024 / 12 / 23,
                        "start_date": 2024 / 12 / 23,
                        "catatan": "ini catatatn ",
                        "file_name": "filenname.jpg",
                        "modified_at": 2024 / 12 / 23,
                    },
                    "jum": 10,
                },
                "meta": {},
                "success": True,
                "message": "Success",
                "code": 200,
            }
        }


# async def get_target(data:GetTargetModel ,payload=Depends(Autentication()), session=Depends(get_db_session)):
#     access = 0
#     divisi = ""

#     # ambill id payload
#     user_id = payload.get('uid', 0)
#     user_data = session.execute(sa.select(User.access,User.divisi).where(User.id_karyawan == user_id)).fetchone()
#     print(user_data)
#     if  user_data.access < 2 :
#         raise HTTPException(400, detail='User not have access')

#     target = session.execute(sa.text(f'SELECT * FROM target WHERE id_target = {data.id_target}')).fetchone()

#     if not target :
#         raise HTTPException(400, detail='Target Tidak tersedia')


#     target_ =  TargetModel(
#                     id_target = target.id_target,
#                     judul = target.judul,
#                     kpi= target.kpi,
#                     deskripsi=target.deskripsi,
#                     start_date = target.start_date,
#                     modified_at = target.modified_at,
#                     deadline = target.deadline,
#                     catatan = target.catatan,
#                     file_name = target.file_name,
#                     id_divisi = target.id_divisi,
#                     status = target.status,
#                     prioritas = target.prioritas,
#                     progres = target.progres
#             )

#     return GetDataTargetResponseModel(
#         data=target_)

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.target import Target
from app.models.user import User
from app.api_models.target_model import TargetModel
from app.api_models import BaseResponseModel
from pydantic import BaseModel


class GetTargetModel(BaseModel):
    id_target: int


class GetDataTargetResponseModel(BaseResponseModel):
    data: TargetModel

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "id_target": 1,
                    "judul": "Target Omset 200jt",
                    "kpi": "Omset",
                    "deskripsi": "Deskripsi Target Omset",
                    "start_date": "2024-01-01",
                    "modified_at": "2024-01-01",
                    "deadline": "2024-12-31",
                    "catatan": "Catatan tambahan",
                    "file_name": "target_omset.jpg",
                    "id_divisi": 1,
                    "nama_divisi": "Divisi Penjualan",
                    "status": 1,
                    "prioritas": 3,
                    "progres": 50,
                },
                "meta": {},
                "success": True,
                "message": "Success GET Target",
                "code": 200,
            }
        }


async def get_target(
    data: GetTargetModel,
    payload=Depends(Autentication()),
    session: Session = Depends(get_db_session),
):
    try:
        # Ambil id payload
        user_id = payload.get("uid", 0)
        user_data = session.query(User).filter(User.id_karyawan == user_id).first()

        if not user_data or user_data.access < 2:
            raise HTTPException(400, detail="User does not have access")

        # Query target dengan relasi ke divisi
        target = (
            session.query(Target).filter(Target.id_target == data.id_target).first()
        )

        if not target:
            raise HTTPException(400, detail="Target not available")

        # Mapping data target
        target_data = TargetModel(
            id_target=target.id_target,
            judul=target.judul,
            kpi=target.kpi,
            deskripsi=target.deskripsi,
            start_date=target.start_date,
            modified_at=target.modified_at,
            deadline=target.deadline,
            catatan=target.catatan,
            file_name=target.file_name,
            id_divisi=target.id_divisi,
            nama_divisi=target.divisi.nama_divisi,
            status=target.status,
            prioritas=target.prioritas,
            progres=target.progres,
        )

        # Mengembalikan data target beserta nama divisi dari relasi
        return GetDataTargetResponseModel(
            data=target_data, success=True, message="Success GET Target", code=200
        )

    except HTTPException as e:
        # Menangani HTTPException yang dilemparkan
        raise e
    except Exception as e:
        # Menangani kesalahan tak terduga
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching the target: {str(e)}",
        )
