from typing import List, Optional

import sqlalchemy as sa
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from app.api_models import BaseResponseModel
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.catatan_target import CatatanTarget

from fastapi.responses import JSONResponse


class DataGetCatatanTarget(BaseModel):
    id_catatan: int


class GetCatatanTargetResponseModel(BaseModel):
    catatan: str


class GetDataCatatanTargetResponseModel(BaseResponseModel):
    data: GetCatatanTargetResponseModel

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "data": [
                        {"id_catatan": 9, "id_target": 3, "catatan": "bla bla bla"}
                    ],
                    "jum": 10,
                },
                "meta": {},
                "success": True,
                "message": "Success",
                "code": 200,
            }
        }


async def get_catatan_target(
    request: DataGetCatatanTarget,
    payload=Depends(Autentication()),
    session=Depends(get_db_session),
):
    try:
        response = session.execute(
            sa.select(CatatanTarget.catatan).where(
                CatatanTarget.id_catatan == request.id_catatan
            )
        ).scalar()

        if response is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Catatan with id {request.id_catatan} not found",
            )

        return GetDataCatatanTargetResponseModel(
            data=GetCatatanTargetResponseModel(catatan=response),
            message="Data catatan berhasil diambil",
            success=True,
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
