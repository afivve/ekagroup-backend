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


class UploadReportTargetDataResponseModel(BaseModel):
    file_name: str


class UploadReportTargetResponseModel(BaseResponseModel):
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


async def upload_report_target(file: UploadFile, session=Depends(get_db_session)):

    # print(id_renker)
    print(file.content_type)
    type = file.content_type.split("/")
    filename = file.filename

    print(filename)

    with open(f"file_report/target/{filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        return UploadReportTargetResponseModel(file_name=filename)
