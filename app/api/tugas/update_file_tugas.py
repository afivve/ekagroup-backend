import os
import random
import shutil

import sqlalchemy as sa
from fastapi import Depends, File, UploadFile
from pydantic import BaseModel

from app.api_models import BaseResponseModel
from app.dependencies.get_db_session import get_db_session
from app.models.tugas import Tugas


class UploadFileData(BaseModel):
    id_tugas: int


class UploadPpDataResponseModel(BaseModel):
    file_name: str


class UploadPpResponseModel(BaseResponseModel):
    file_name: str

    class Config:
        json_schema_extra = {
            "example": {
                "data": {"file_name": "asasda.jpg"},
                "meta": {},
                "success": True,
                "message": "Success",
                "code": 200,
            }
        }


async def upload_report_tugas(file: UploadFile, session=Depends(get_db_session)):

    datanya = session.execute(
        sa.select(Tugas.file_name).where(Tugas.file_name == "coba")
    ).scalar()

    print(datanya)
    # if datanya != "NULL":
    #     os.remove("file_report/tugas/"+"coba.jpg")
    print(file.filename)
    print(file.content_type)
    type = file.content_type.split("/")
    rand = random.randint(1000, 9999)
    filename = file.filename

    with open(f"file_report/tugas/{filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        return UploadPpResponseModel(file_name=filename)
