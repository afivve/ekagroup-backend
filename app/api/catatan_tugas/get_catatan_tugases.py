from typing import List
from fastapi import Depends, HTTPException, status
import sqlalchemy as sa
from pydantic import BaseModel

from app.api_models import BaseResponseModel
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.catatan_tugas import CatatanTugas
from app.models.tugas import Tugas  # Pastikan mengimpor model Tugas


class DataGetCatatanTugases(BaseModel):
    id_tugas: int


class Catatan(BaseModel):
    id_catatan: int
    catatan: str
    id_tugas: int
    id_karyawan: str  # Menambahkan id_karyawan pada model response


class GetCatatanTugasesResponseModel(BaseModel):
    data: List[Catatan]


class GetDataCatatanTugasesResponseModel(BaseResponseModel):
    data: GetCatatanTugasesResponseModel

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "data": [
                        {
                            "id_catatan": 9,
                            "id_tugas": 3,
                            "id_karyawan": "A015",
                            "catatan": "bla bla bla",
                        }
                    ],
                    "jum": 10,
                },
                "meta": {},
                "success": True,
                "message": "Success",
                "code": 200,
            }
        }


async def get_catatan_tugases(
    request: DataGetCatatanTugases,
    payload=Depends(Autentication()),
    session=Depends(get_db_session),
):
    try:
        # Query untuk mendapatkan catatan_tugas dan tugas yang relevan
        response = session.execute(
            sa.select(
                CatatanTugas.id_catatan,
                CatatanTugas.catatan,
                Tugas.id_tugas,
                Tugas.id_karyawan,  # Mengambil id_karyawan dari relasi Tugas
            )
            .join(Tugas, Tugas.id_tugas == CatatanTugas.id_tugas)
            .where(CatatanTugas.id_tugas == request.id_tugas)
        ).all()

        # Map hasil query ke model Catatan
        datalist = [
            Catatan(
                id_catatan=catatan.id_catatan,
                catatan=catatan.catatan,
                id_tugas=catatan.id_tugas,
                id_karyawan=catatan.id_karyawan,
            )
            for catatan in response
        ]

        # Return response dengan data yang diambil
        return GetDataCatatanTugasesResponseModel(
            data=GetCatatanTugasesResponseModel(data=datalist)
        )

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving catatan tugas: {str(e)}",
        )
