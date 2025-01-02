from typing import Optional
import sqlalchemy as sa
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from app.api_models import BaseResponseModel
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.catatan_renker import CatatanRenker

from fastapi.responses import JSONResponse


class DataGetCatatanRenker(BaseModel):
    id_catatan: int


class GetCatatanRenkerResponseModel(BaseModel):
    catatan: str


class GetDataCatatanRenkerResponseModel(BaseResponseModel):
    data: GetCatatanRenkerResponseModel

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "data": [
                        {
                            "id_catatan": 9,
                            "id_renker": 3,
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


async def get_catatan_renker(
    request: DataGetCatatanRenker,
    payload=Depends(Autentication()),
    session=Depends(get_db_session),
):
    try:

        query = sa.select(CatatanRenker.catatan).where(
            CatatanRenker.id_catatan == request.id_catatan
        )
        result = session.execute(query).scalar()

        return GetDataCatatanRenkerResponseModel(
            data=GetCatatanRenkerResponseModel(catatan=result),
            success=True,
            message="Sukses mengambil Data Catatan Rencana Kerja Berdasarkan ID",
            code=200,
        )

    except Exception as e:
        print(f"Error occurred: {str(e)}")

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Internal server error",
                "code": 500,
            },
        )
