from typing import List, Optional
import sqlalchemy as sa
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from app.api_models import BaseResponseModel
from app.api_models.rencana_kerja_model import RencanaKerjaModel
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.user import User
from app.models.rencana_kerja import RencanaKerja


class GetRencanaKerjaModel(BaseModel):
    id_renker: int


class GetRencanaKerjaDataResponseModel(BaseResponseModel):
    data: RencanaKerjaModel

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "data": {
                        "id_renker": 1,
                        "id_target": 1,
                        "judul": "omset 200 jt per bulan",
                        "id_divisi": 2,
                        "deskripsi": "harus omset 200 jt per bulan",
                        "kpi": "ommset",
                        "deadline": "2024-12-23",
                        "start_date": "2024-12-23",
                        "catatan": "ini catatan",
                        "file_name": "filenname.jpg",
                        "modified_at": "2024-12-23",
                    }
                },
                "meta": {},
                "success": True,
                "message": "Success",
                "code": 200,
            }
        }


async def get_rencana_kerja(
    data: GetRencanaKerjaModel,
    payload=Depends(Autentication()),
    session=Depends(get_db_session),
):
    try:
        # Ambil id payload
        user_id = payload.get("uid", 0)

        # Periksa apakah user valid
        user_data = session.query(User).filter(User.id_karyawan == user_id).first()

        if not user_data:
            raise HTTPException(400, detail="User not found")

        # Periksa akses user
        if user_data.access < 2:
            raise HTTPException(403, detail="User does not have sufficient access")

        # Query untuk mendapatkan rencana kerja berdasarkan id_renker
        renker = (
            session.query(RencanaKerja)
            .filter(RencanaKerja.id_renker == data.id_renker)
            .first()
        )

        if not renker:
            raise HTTPException(404, detail="Rencana Kerja tidak tersedia")

        # Mapping data ke model response
        rencana_ = RencanaKerjaModel(
            id_renker=renker.id_renker,
            id_target=renker.id_target,
            judul=renker.judul,
            kpi=renker.kpi,
            deskripsi=renker.deskripsi,
            start_date=renker.start_date,
            modified_at=renker.modified_at,
            deadline=renker.deadline,
            catatan=renker.catatan,
            file_name=renker.file_name,
            id_divisi=renker.id_divisi,
            status=renker.status,
            prioritas=renker.prioritas,
            progres=renker.progres,
            nama_divisi=renker.divisi.nama_divisi,
        )

        return GetRencanaKerjaDataResponseModel(data=rencana_)

    except HTTPException as e:
        # Tangani pengecualian HTTP yang sudah didefinisikan sebelumnya
        raise e

    except Exception as e:
        # Tangani kesalahan tak terduga lainnya
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


# async def get_rencana_kerja(data:GetRencanaKerjaModel ,payload=Depends(Autentication()), session=Depends(get_db_session)):
#     access = 0
#     divisi = ""

#     # ambill id payload
#     user_id = payload.get('uid', 0)
#     user_data = session.execute(sa.select(User.access,User.divisi).where(User.id_karyawan == user_id)).fetchone()
#     print(user_data)
#     if  user_data.access < 2 :
#         raise HTTPException(400, detail='User not have access')

#     renker = session.execute(sa.text(f'SELECT * FROM rencana_kerja WHERE id_renker = {data.id_renker}')).fetchone()

#     if len(renker) == 0:
#         raise HTTPException(400, detail='Target Tidak tersedia')


#     rencana_ =  RencanaKerjaModel(
#                     id_renker = renker.id_renker,
#                     id_target = renker.id_target,
#                     judul = renker.judul,
#                     kpi= renker.kpi,
#                     deskripsi=renker.deskripsi,
#                     start_date = renker.start_date,
#                     modified_at = renker.modified_at,
#                     deadline = renker.deadline,
#                     catatan = renker.catatan,
#                     file_name = renker.file_name,
#                     id_divisi = renker.id_divisi,
#                     status = renker.status,
#                     prioritas=renker.prioritas,
#                     progres=renker.progres
#             )


#     return GetRencanaKerjaDataResponseModel(
#         data=rencana_)
