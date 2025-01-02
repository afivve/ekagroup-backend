from typing import List
import sqlalchemy as sa
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_models import BaseResponseModel
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.catatan_renker import CatatanRenker

from fastapi.responses import JSONResponse


class DataGetCatatanRenkeres(BaseModel):
    id_renker: int


class Catatan(BaseModel):
    id_catatan: int
    catatan: str


class GetCatatanRenkeresResponseModel(BaseModel):
    data: List[Catatan]


class GetDataCatatanRenkeresResponseModel(BaseResponseModel):
    data: GetCatatanRenkeresResponseModel

    class Config:
        json_schema_extra = {
            "example": {
                "data": {"data": [{"id_catatan": 9, "catatan": "bla bla bla"}]},
                "meta": {},
                "success": True,
                "message": "Success",
                "code": 200,
            }
        }


async def get_catatan_renkers(
    request: DataGetCatatanRenkeres,
    payload=Depends(Autentication()),
    session: AsyncSession = Depends(get_db_session),
) -> GetDataCatatanRenkeresResponseModel:

    try:

        query = (
            sa.select(CatatanRenker.id_catatan, CatatanRenker.catatan)
            .where(CatatanRenker.id_renker == request.id_renker)
            .order_by(CatatanRenker.id_catatan.desc())
        )
        result = session.execute(query)
        response = result.all()

        datalist = [
            Catatan(id_catatan=row.id_catatan, catatan=row.catatan) for row in response
        ]

        return GetDataCatatanRenkeresResponseModel(
            data=GetCatatanRenkeresResponseModel(data=datalist),
            success=True,
            message="Catatan rencana kerja fetched successfully",
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
