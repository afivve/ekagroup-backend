# import sqlalchemy as sa
# from fastapi import Depends
# from pydantic import BaseModel

# from app.api_models import BaseResponseModel
# from app.api_models.divisi_model import DivisiModel
# from app.api_models.profile_model import ProfileModel
# from app.config import config
# from app.dependencies.autentication import Autentication
# from app.dependencies.get_db_session import get_db_session
# from app.models.divisi import Divisi
# from app.models.user import User


# class GetDivisiData(BaseModel):
#     id_divisi : int

# class GetDivisiDataResponseModel(BaseResponseModel):
#     data: DivisiModel

#     class Config:
#         json_schema_extra = {
#             'example': {
#                 'data':
#                         {   "id_divisi":1,
#                             "nama_divisi":"Agro Bisnnis",
#                             "jml_karyawan":29,
#                             "manager":{
#                                 "id_karyawan":"Alpen"
#                             }
#                         },
#                 'meta': {},
#                 'success': True,
#                 'message': 'Success',
#                 'code': 200
#             }
#         }


# async def get_divisi(data:GetDivisiData,payload=Depends(Autentication()), session=Depends(get_db_session)):
#     divisi = session.execute(sa.select(Divisi.id_divisi,Divisi.nama_divisi,Divisi.path_foto).where(Divisi.id_divisi == data.id_divisi)).fetchone()


#     def jml_karyawan(x:int):
#         jumlah_karyawans = session.execute(sa.text(f"select count(id_karyawan) as jml_karyawan from user where divisi = {x} ")).fetchone()
#         return jumlah_karyawans.jml_karyawan

#     def manager(x:int):
#         profile =  session.execute(sa.select(
#                 User.id_karyawan,
#                 User.username,
#                 User.full_name,
#                 User.email,
#                 User.noWa,
#                 User.nik,
#                 User.alamat,
#                 User.access,
#                 User.path_foto,
#                 User.divisi,
#                 User.jabatan
#             ).where(
#             sa.and_( User.divisi == x , User.access >2)
#             )
#             ).fetchone()

#         if not profile :
#             return

#         manger_nya = ProfileModel(
#             id_karyawan= profile.id_karyawan,
#             username=profile.username,
#             full_name=profile.full_name,
#             email=profile.email,
#             noWa=profile.noWa,
#             access=profile.access,
#             path_foto=profile.path_foto,
#             nik=profile.nik,
#             alamat=profile.alamat,
#             divisi=profile.divisi,
#             jabatan=profile.jabatan,
#             nama_divisi='x'
#             )
#         return manger_nya


#     div =   DivisiModel(
#                 id_divisi=divisi.id_divisi,
#                 nama_divisi=divisi.nama_divisi,
#                 path_foto='',
#                 jml_karyawan = jml_karyawan(divisi.id_divisi),
#                 manager=manager(divisi.id_divisi)
#             )
#     return GetDivisiDataResponseModel(
#         data=div)

from sqlalchemy.orm import joinedload
from fastapi import Depends, HTTPException, status
import sqlalchemy as sa
from app.models.divisi import Divisi
from app.api_models import BaseResponseModel
from app.dependencies.get_db_session import get_db_session
from app.dependencies.autentication import Autentication
from pydantic import BaseModel


class GetDivisiData(BaseModel):
    id_divisi: int


class GetDivisiDataResponseModel(BaseResponseModel):
    data: dict

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "divisi": {
                        "id_divisi": 1,
                        "nama_divisi": "Agro Bisnis",
                        "jml_karyawan": 29,
                        "manager": {"id_karyawan": "Alpen"},
                        "path_foto": "/path/to/foto",
                    },
                    "karyawans": [
                        {
                            "id_karyawan": 1,
                            "nama": "Karyawan 1",
                            "jabatan": "Manager",
                            "email": "karyawan1@example.com",
                        },
                        {
                            "id_karyawan": 2,
                            "nama": "Karyawan 2",
                            "jabatan": "Staff",
                            "email": "karyawan2@example.com",
                        },
                    ],
                },
                "meta": {},
                "success": True,
                "message": "Success",
                "code": 200,
            }
        }


async def get_divisi(
    data: GetDivisiData,
    payload=Depends(Autentication()),
    session=Depends(get_db_session),
):
    try:
        # Query the Divisi data along with its related users (joinedload)
        divisi = (
            session.execute(
                sa.select(Divisi)
                .options(
                    joinedload(Divisi.user),  # Eager load the 'user' relation
                )
                .where(Divisi.id_divisi == data.id_divisi)
            )
            .scalars()
            .first()
        )  # Get the first matching Divisi object

        # if not divisi:
        #     # If divisi is not found, raise a 404 error
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND, detail="Divisi not found"
        #     )

        # Determine the manager of the divisi
        manager = None
        for user in divisi.user:
            if user.access > 2:  # Manager usually has access > 2
                manager = {
                    "id_karyawan": user.id_karyawan,
                    "full_name": user.full_name,
                    "email": user.email,
                    "jabatan": user.jabatan,
                    "path_foto": user.path_foto or "",
                }
                break

        # Prepare the divisi data
        divisi_data = {
            "divisi": {
                "id_divisi": divisi.id_divisi,
                "nama_divisi": divisi.nama_divisi,
                "path_foto": divisi.path_foto or "",
                "jml_karyawan": len(divisi.user),
                "manager": manager,
            },
            "karyawans": [
                {
                    "id_karyawan": user.id_karyawan,
                    "nama": user.full_name,
                    "jabatan": user.jabatan,
                    "email": user.email,
                }
                for user in divisi.user
            ],
        }

        return GetDivisiDataResponseModel(
            data=divisi_data, success=True, message="Success", code=200
        )

    except HTTPException as e:
        # If it's an HTTPException (like 404), re-raise it
        raise e

    except Exception as e:
        # For any unexpected errors, return a 500 Internal Server Error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )
