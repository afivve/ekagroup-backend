from typing import List
from sqlalchemy.orm import joinedload
from fastapi import Depends, HTTPException, status
from sqlalchemy import select

from app.api_models import BaseResponseModel
from app.api_models.profile_model import ProfileModel
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.divisi import Divisi
from app.models.user import User
from app.api_models.divisi_model import DivisiModel


class GetDataDivisiesResponseModel(BaseResponseModel):
    data: List[object]

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "data": [
                        {
                            "id_divisi": 2,
                            "nama_divisi": "Agro Bisnis",
                            "path_foto": "/path/to/foto",
                            "jml_karyawan": 5,
                            "manager": {
                                "id_karyawan": "123",
                                "full_name": "Manager 1",
                                "jabatan": "Manager",
                                "email": "manager1@example.com",
                            },
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


async def get_divisies(
    payload=Depends(Autentication()), session=Depends(get_db_session)
):
    try:
        # Ambil divisies dengan relasi 'user' yang sudah diload
        divisies = (
            session.execute(
                select(Divisi).options(
                    joinedload(Divisi.user)
                )  # Eager load relasi 'user' pada setiap divisi
            )
            .scalars()
            .unique()
            .all()
        )  # Pastikan hasilnya unik dengan .unique()

        # If no divisies are found
        # if not divisies:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND, detail="No divisies found"
        #     )

        # Helper function to count the number of users in a division
        def jml_karyawan(divisi):
            return len(divisi.user)

        # Helper function to find the manager in a division
        def manager(divisi):
            # Filter user with access > 2 to find manager
            manager_user = next((user for user in divisi.user if user.access > 2), None)
            if manager_user:
                return ProfileModel(
                    id_karyawan=manager_user.id_karyawan,
                    username=manager_user.username,
                    full_name=manager_user.full_name,
                    email=manager_user.email,
                    noWa=manager_user.noWa,
                    access=manager_user.access,
                    path_foto=manager_user.path_foto,
                    nik=manager_user.nik,
                    alamat=manager_user.alamat,
                    divisi=manager_user.divisi_id,
                    jabatan=manager_user.jabatan,
                    nama_divisi=divisi.nama_divisi,
                )
            return None

        # Process each divisi and prepare the data
        data_list = [
            DivisiModel(
                id_divisi=divisi.id_divisi,
                nama_divisi=divisi.nama_divisi,
                path_foto=divisi.path_foto,
                jml_karyawan=jml_karyawan(divisi),
                manager=manager(divisi),
            )
            for divisi in divisies
        ]

        return GetDataDivisiesResponseModel(
            data=data_list, success=True, message="Success", code=200
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
