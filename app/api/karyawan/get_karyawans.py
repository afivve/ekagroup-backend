from typing import List, Optional

import jwt
import sqlalchemy as sa
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.api_models import BaseResponseModel
from app.config import config
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session

from app.utils.generate_hash import generate_hash


class DataGetKaryawan(BaseModel):
    # mode: Optional[str] = None
    index: Optional[int] = None
    # part: Optional[int] = None
    nama: Optional[str] = None
    divisi: Optional[str] = None


class GetKaryawansResponseModel(BaseModel):
    data: List[object]
    jum: int


class GetDataKaryawansResponseModel(BaseResponseModel):
    data: GetKaryawansResponseModel

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "data": [
                        {
                            "nik": "140416160400****",
                            "nama": "Alfan nurchamid",
                            "username": "Alpen",
                            "divisi": "Marketing",
                            "jabatan": "IT",
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


async def get_karyawans(
    request: DataGetKaryawan,
    payload=Depends(Autentication()),
    session=Depends(get_db_session),
):
    survey = True
    profile_data = jsonable_encoder(request)
    part = "   "
    index: int = 0
    if "index" in profile_data and profile_data["index"]:
        index = profile_data["index"]

    if "nama" in profile_data and profile_data["nama"]:
        nama = profile_data["nama"]
        part = f"AND full_name LIKE '%{nama}%'"
        index = 0
        print(nama, part)
    if "divisi" in profile_data and profile_data["divisi"]:
        part = f"AND divisi = {profile_data['divisi']}"

    datalist = []

    awal = index * 5
    akhir = awal + 4

    awal = str(awal)
    akhir = str(akhir)

    sql = f"SELECT * FROM (SELECT ROW_NUMBER() OVER (ORDER BY full_name DESC) AS R, full_name,nik , jabatan, divisi ,id_karyawan FROM user WHERE nik!=''  {part}) AS TR WHERE  R BETWEEN {awal} AND {akhir};"

    karyawans = session.execute(sa.text(sql))

    for p in karyawans:

        hnik = p.nik[0:8] + "xxxxxxxxxx"

        datalist.append(
            {
                "nik": hnik,
                "nama": p.full_name,
                "divisi": p.divisi,
                "jabatan": p.jabatan,
                "id_karyawan": p.id_karyawan,
            }
        )
    jum = len(datalist)
    # print(datalist)

    return GetDataKaryawansResponseModel(
        data=GetKaryawansResponseModel(data=datalist, jum=jum)
    )
