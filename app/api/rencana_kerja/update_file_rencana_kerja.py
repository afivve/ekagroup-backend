# import os
# import random
# import shutil

# import sqlalchemy as sa
# from fastapi import Depends, File, UploadFile
# from pydantic import BaseModel

# from app.api_models import BaseResponseModel
# from app.dependencies.get_db_session import get_db_session
# from app.models.tugas import Tugas

# class UploadFileData(BaseModel):
#     id_renker : int

# class UploadReportRencanaKerjaDataResponseModel(BaseModel):
#     file_name: str

# class UploadReportRencanaKerjaResponseModel(BaseResponseModel):
#     file_name: str

#     class Config:
#         json_schema_extra = {
#             'example': {
#                 'data': {
#                     'file_name': 'asasda.jpg'
#                 },
#                 'meta': {},
#                 'success': True,
#                 'message': 'Success',
#                 'code': 200
#             }
#         }


# async def upload_report_rencana_kerja(file: UploadFile, session=Depends(get_db_session)):

#     # print(id_renker)
#     print(file.content_type)
#     type = file.content_type.split('/')
#     filename = file.filename+'.'+type[1]
#     print(filename)

#     with open(f'file_report/rencana_kerja/{filename}', 'wb') as buffer:
#         shutil.copyfileobj(file.file, buffer)
#         return UploadReportRencanaKerjaResponseModel(
#                 file_name=filename
#             )

import os
import shutil
from fastapi import Depends, UploadFile, HTTPException
from pydantic import BaseModel
from app.dependencies.get_db_session import get_db_session
from app.api_models import BaseResponseModel


class UploadFileData(BaseModel):
    id_renker: int


class UploadReportRencanaKerjaDataResponseModel(BaseModel):
    file_name: str


class UploadReportRencanaKerjaResponseModel(BaseResponseModel):
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


async def upload_report_rencana_kerja(
    file: UploadFile, session=Depends(get_db_session)
):
    try:
        # Verifikasi tipe file (untuk memastikan file adalah gambar atau dokumen yang valid)
        if file.content_type.split("/")[0] not in ["image", "application"]:
            raise HTTPException(400, detail="Format file tidak didukung")

        # Tentukan nama file dengan ekstensi yang benar
        file_extension = file.content_type.split("/")[1]
        filename = f"{file.filename}.{file_extension}"

        # Tentukan path direktori tempat file disimpan
        file_path = os.path.join("file_report", "rencana_kerja", filename)

        # Pastikan direktori tujuan ada
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Simpan file ke direktori yang sudah ditentukan
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Kembalikan respons dengan nama file yang telah diupload
        return UploadReportRencanaKerjaResponseModel(file_name=filename)

    except Exception as e:
        # Tangani kesalahan tak terduga
        raise HTTPException(
            status_code=500, detail=f"Terjadi kesalahan saat mengunggah file: {str(e)}"
        )
