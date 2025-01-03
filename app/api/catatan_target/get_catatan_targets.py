from typing import List

import sqlalchemy as sa
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from app.api_models import BaseResponseModel
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.catatan_target import CatatanTarget


class DataGetCatatanTargets(BaseModel):
    id_target: int


class Catatan(BaseModel):
    id_catatan: int
    catatan: str


class GetCatatanTargetsResponseModel(BaseModel):
    data: List[Catatan]


class GetDataCatatanTargetsResponseModel(BaseResponseModel):
    data: GetCatatanTargetsResponseModel

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


async def get_catatan_targets(
    request: DataGetCatatanTargets,
    payload=Depends(Autentication()),
    session=Depends(get_db_session),
):
    try:
        # Query to fetch notes based on id_target
        response = session.execute(
            sa.select(CatatanTarget.id_catatan, CatatanTarget.catatan).where(
                CatatanTarget.id_target == request.id_target
            )
        ).all()

        # If no data is found, raise a 404 error
        # if len(response) == 0:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND, detail="Target not available"
        #     )

        # Build the list of Catatan objects
        datalist = [
            Catatan(id_catatan=catatan.id_catatan, catatan=catatan.catatan)
            for catatan in response
        ]

        # Return the response in the required format
        return GetDataCatatanTargetsResponseModel(
            data=GetCatatanTargetsResponseModel(data=datalist),
            message="Data catatan berhasil diambil untuk target ini.",
            success=True,
            code=200,
        )

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
