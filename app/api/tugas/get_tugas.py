from typing import List, Optional

import sqlalchemy as sa
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.future import select

from app.api_models import BaseResponseModel
from app.api_models.tugas_model import TugasModel
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.user import User
from app.models.tugas import Tugas


class GetTugasModel(BaseModel):
    id_tugas: int


class GetTugasDataResponseModel(BaseResponseModel):
    data: TugasModel

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "id_tugas": 1,
                    "id_renker": 1,
                    "id_target": 1,
                    "judul": "Omset 200jt per bulan",
                    "id_divisi": 2,
                    "deskripsi": "Harus omset 200 jt per bulan",
                    "kpi": "Omset",
                    "deadline": "2024-12-23",
                    "start_date": "2024-12-23",
                    "catatan": "Ini catatan",
                    "file_name": "filename.jpg",
                    "modified_at": "2024-12-23",
                    "pelaksana": "John Doe",
                    "nama_divisi": "Divisi Penjualan",
                    "status": 1,
                    "prioritas": 3,
                    "progres": 50,
                },
                "meta": {},
                "success": True,
                "message": "Success",
                "code": 200,
            }
        }


async def get_tugas(
    data: GetTugasModel,
    payload=Depends(Autentication()),
    session=Depends(get_db_session),
):
    try:

        user_id = payload.get("uid", 0)
        # user_data = session.query(User).filter(User.id_karyawan == user_id).first()

        # if not user_data:
        #     raise HTTPException(404, detail="User not found")

        # if user_data.access < 2:
        #     raise HTTPException(403, detail="User does not have access")

        tugas = session.query(Tugas).filter(Tugas.id_tugas == data.id_tugas).first()

        # if not tugas:
        #     raise HTTPException(404, detail="Tugas tidak tersedia")

        pelaksana = (
            session.query(User.full_name)
            .filter(User.id_karyawan == tugas.id_karyawan)
            .scalar()
        )

        tugas_ = TugasModel(
            id_tugas=tugas.id_tugas,
            id_renker=tugas.id_renker,
            judul=tugas.judul,
            kpi=tugas.kpi,
            deskripsi=tugas.deskripsi,
            start_date=tugas.start_date,
            modified_at=tugas.modified_at,
            deadline=tugas.deadline,
            catatan=tugas.catatan,
            file_name=tugas.file_name,
            id_divisi=tugas.id_divisi,
            status=tugas.status,
            id_karyawan=tugas.id_karyawan,
            prioritas=tugas.prioritas,
            progres=tugas.progres,
            pelaksana=pelaksana,
            nama_divisi=tugas.divisi.nama_divisi,
        )

        return GetTugasDataResponseModel(data=tugas_)

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving catatan tugas: {str(e)}",
        )


# async def get_tugas(data:GetTugasModel ,payload=Depends(Autentication()), session=Depends(get_db_session)):
#     access = 0
#     divisi = ""

#     # ambill id payload
#     user_id = payload.get('uid', 0)
#     user_data = session.execute(sa.select(User.access,User.divisi).where(User.id_karyawan == user_id)).fetchone()
#     print(user_data)
#     if  user_data.access < 2 :
#         raise HTTPException(400, detail='User not have access')

#     tugas = session.execute(sa.text(f'SELECT * FROM tugas WHERE id_tugas = {data.id_tugas}')).fetchone()

#     if tugas and len(tugas) == 0:
#         raise HTTPException(400, detail='Target Tidak tersedia')

#     def pelaksana(id_karyawan):
#         print(id_karyawan)
#         profile = session.execute(
#         sa.select(
#             User.full_name
#         ).where(
#             User.id_karyawan == id_karyawan
#         )
#         ).scalar()
#         return profile

#     tugas_ =  TugasModel(
#                     id_tugas = tugas.id_tugas,
#                     id_renker = tugas.id_renker,
#                     judul = tugas.judul,
#                     kpi= tugas.kpi,
#                     deskripsi=tugas.deskripsi,
#                     start_date = tugas.start_date,
#                     modified_at = tugas.modified_at,
#                     deadline = tugas.deadline,
#                     catatan = tugas.catatan,
#                     file_name = tugas.file_name,
#                     id_divisi = tugas.id_divisi,
#                     status = tugas.status,
#                     id_karyawan = tugas.id_karyawan,
#                     prioritas = tugas.prioritas,
#                     progres = tugas.progres,
#                     pelaksana=pelaksana(tugas.id_karyawan)


#             )


#     return GetTugasDataResponseModel(
#         data=tugas_)
