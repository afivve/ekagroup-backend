from typing import List, Optional

from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import and_

from app.api_models import BaseResponseModel
from app.api_models.tugas_model import TugasModel
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.tugas import Tugas
from app.models.user import User
from sqlalchemy.orm import joinedload


class GetTugasData(BaseModel):
    id_divisi: Optional[int] = None
    id_renker: Optional[int] = None
    id_karyawan: Optional[str] = None
    bebas: int


class GetDatatuugassResponseModel(BaseResponseModel):
    data: List[TugasModel]

    class Config:
        json_schema_extra = {
            "example": {
                "data": [
                    {
                        "id_renker": 2,
                        "id_tugas": 1,
                        "judul": "Omset 200 jt per bulan",
                        "id_divisi": 2,
                        "deskripsi": "Harus omset 200 jt per bulan",
                        "kpi": "Omset",
                        "deadline": "2024-12-23",
                        "start_date": "2024-12-23",
                        "catatan": "Ini catatan",
                        "file_name": "filename.jpg",
                        "modified_at": "2024-12-23",
                    }
                ],
                "jum": 10,
                "meta": {},
                "success": True,
                "message": "Success",
                "code": 200,
            }
        }


async def get_tugases(
    data: GetTugasData,
    payload=Depends(Autentication()),
    session=Depends(get_db_session),
):
    try:
        user_id = payload.get("uid", 0)
        user_data = session.query(User).filter(User.id_karyawan == user_id).first()

        if not user_data:
            raise HTTPException(404, detail="User not found")

        if user_data.access == 0:
            raise HTTPException(403, detail="User does not have access")

        filters = []
        if user_data.access < 3:
            if data.id_divisi:
                raise HTTPException(
                    400, detail=f"User not have access to divisi {data.id_divisi}"
                )
            filters.append(Tugas.id_divisi == user_data.divisi.id_divisi)
        elif user_data.access >= 3 and data.id_divisi:
            filters.append(Tugas.id_divisi == data.id_divisi)

        if data.id_renker:
            filters.append(Tugas.id_renker == data.id_renker)
        if data.id_karyawan:
            filters.append(Tugas.id_karyawan == data.id_karyawan)

        # Use joinedload to eagerly load the `Divisi` relationship
        tugases_query = (
            session.query(Tugas)
            .options(joinedload(Tugas.divisi))
            .filter(and_(*filters))
        )
        tugases = tugases_query.all()

        if not tugases:
            raise HTTPException(404, detail="No tasks found")

        def pelaksana(id_karyawan):
            return (
                session.query(User.full_name)
                .filter(User.id_karyawan == id_karyawan)
                .scalar()
            )

        data_list = [
            TugasModel(
                id_tugas=tugas.id_tugas,
                id_renker=tugas.id_renker,
                judul=tugas.judul,
                kpi=tugas.kpi,
                deskripsi=tugas.deskripsi,
                start_date=tugas.start_date,
                modified_at=tugas.modified_at,
                deadline=tugas.deadline,
                catatan=tugas.catatan,
                file_name=tugas.file_name,
                id_divisi=tugas.id_divisi,
                status=tugas.status,
                id_karyawan=tugas.id_karyawan,
                prioritas=tugas.prioritas,
                progres=tugas.progres,
                pelaksana=pelaksana(tugas.id_karyawan),
                nama_divisi=tugas.divisi.nama_divisi,  # Access related data safely
            )
            for tugas in tugases
        ]

        return GetDatatuugassResponseModel(data=data_list)

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving catatan tugas: {str(e)}",
        )


# async def get_tugases(data:GetTugasData,payload=Depends(Autentication()), session=Depends(get_db_session)):
#     access = 0
#     param =""
#     def cek_param(panjang):
#         if panjang > 0 :
#             return ' AND '
#         else :
#             return ' WHERE '

#     data_tugas = jsonable_encoder(data)

#     # ambill id payload
#     user_id = payload.get('uid', 0)
#     user_data = session.execute(sa.select(User.access,User.divisi).where(User.id_karyawan == user_id)).fetchone()
#     print(user_data)

#     #  jika akses  ==0 maka akses ditolak
#     if  user_data.access == 0 :
#         raise HTTPException(400, detail='User not have access')
#     #  jika akses < 3 maka sql dibatasi di divisi nya saja
#     elif user_data.access < 3:
#         if data.id_divisi :
#              raise HTTPException(400, detail=f'User not have access {data.id_divisi}')
#         param= f"WHERE id_divisi = {user_data.divisi}"
#     elif user_data.access > 3 and data.id_divisi  :
#         param += cek_param(len(param))
#     #  jika akses > 3 maka sql disesuaikann divisi yg dimminntaa
#         param =f" id_divisi = {data.id_divisi}"

#     if  "id_renker" in data_tugas and data_tugas['id_renker']  :
#         param += cek_param(len(param))
#         param = param + f" id_renker = {data.id_renker}"

#     if data_tugas['id_karyawan'] and 'id_karyawan' in data_tugas :
#         param += cek_param(len(param))
#         param = param + f" id_karyawan ='{data.id_karyawan}'"

#     tugases = session.execute(sa.text(f'SELECT * FROM tugas {param}')).all()

#     def pelaksana(id_karyawan):
#         print(id_karyawan)
#         profile = session.execute(
#         sa.select(
#             User.full_name
#         ).where(
#             User.id_karyawan == id_karyawan
#         )
#         ).scalar()
#         return profile


#     dataLList=[]

#     for tugas in tugases:
#         dataLList.append(
#             TugasModel(
#                    id_tugas = tugas.id_tugas,
#                     id_renker = tugas.id_renker,
#                     judul = tugas.judul,
#                     kpi= tugas.kpi,
#                     deskripsi=tugas.deskripsi,
#                     start_date = tugas.start_date,
#                     modified_at = tugas.modified_at,
#                     deadline = tugas.deadline,
#                     catatan = tugas.catatan,
#                     file_name = tugas.file_name,
#                     id_divisi = tugas.id_divisi,
#                     status = tugas.status,
#                     id_karyawan = tugas.id_karyawan,
#                     prioritas = tugas.prioritas,
#                     progres = tugas.progres,
#                     pelaksana=pelaksana(tugas.id_karyawan)

#             )
#         )


#     return GetDatatuugassResponseModel(
#         data=dataLList)
