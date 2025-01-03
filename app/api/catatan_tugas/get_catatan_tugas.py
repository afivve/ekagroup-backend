from typing import Optional
import sqlalchemy as sa
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from app.api_models import BaseResponseModel
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.catatan_tugas import CatatanTugas


class DataGetCatatanTugas(BaseModel):
    id_catatan: int


class GetCatatanTugasResponseModel(BaseModel):
    catatan: str


class GetDataCatatanTugasResponseModel(BaseResponseModel):
    data: GetCatatanTugasResponseModel

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "data": [
                        {"id_catatan": 9, "id_tugas": 3, "catatan": "bla bla bla"}
                    ],
                    "jum": 10,
                },
                "meta": {},
                "success": True,
                "message": "Success",
                "code": 200,
            }
        }


async def get_catatan_tugas(
    request: DataGetCatatanTugas,
    payload=Depends(Autentication()),
    session=Depends(get_db_session),
):
    try:
        # Query to get the catatan based on id_catatan
        response = session.execute(
            sa.select(CatatanTugas.catatan).where(
                CatatanTugas.id_catatan == request.id_catatan
            )
        ).scalar()

        # Check if the catatan exists
        # if not response:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail=f"Catatan with id {request.id_catatan} not found",
        #     )

        # Return the successful response with the catatan data
        return GetDataCatatanTugasResponseModel(
            data=GetCatatanTugasResponseModel(catatan=response)
        )

    except HTTPException as e:
        # If the exception is HTTPException, re-raise it
        raise e

    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
