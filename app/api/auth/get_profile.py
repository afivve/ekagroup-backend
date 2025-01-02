from typing import List
from fastapi import Depends, HTTPException
import sqlalchemy as sa

from app.api_models import BaseResponseModel
from app.api_models.profile_model import ProfileModel
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session

from app.models.divisi import Divisi
from app.models.user import User


class GetProfileResponseModel(BaseResponseModel):
    data: ProfileModel

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "id_karyawan": "1000",
                    "username": "alpen",
                    "access_token": "access token",
                    "email": "alfannurchamid@gmial.com",
                    "noWa": "089681709727",
                    "access": "0",
                    "path_foto": "skjdalk.jpg",
                    "alamat": "rt1,rw2,ngalian,wadaslintang",
                    "nik": "3307080409009990",
                    "id_divisi": 1,
                    "nama_divisi": "agro bisnis",
                    "jabatan": "staff",
                },
                "meta": {},
                "success": True,
                "message": "Success",
                "code": 200,
            }
        }


async def get_profile(
    payload=Depends(Autentication()), session=Depends(get_db_session)
):
    # Pesimistik: gunakan default 0 jika 'uid' tidak ditemukan
    user_id = payload.get("uid", 0)

    # Query dengan memanfaatkan relasi untuk mengambil profil beserta nama_divisi
    profile = session.query(User).filter(User.id_karyawan == user_id).first()

    if not profile:
        raise HTTPException(status_code=400, detail="User not found")

    # Ambil nama_divisi dari relasi jika ada
    nama_divisi = (
        profile.divisi.nama_divisi if profile.divisi else "Nama Divisi Tidak Diketahui"
    )

    # Kembalikan response model
    return GetProfileResponseModel(
        data=ProfileModel(
            id_karyawan=profile.id_karyawan,
            username=profile.username,
            full_name=profile.full_name,
            email=profile.email,
            noWa=profile.noWa,
            access=profile.access,
            path_foto=profile.path_foto,
            nik=profile.nik,
            alamat=profile.alamat,
            divisi=profile.divisi_id,  # Sesuaikan nama field untuk ID divisi
            jabatan=profile.jabatan,
            nama_divisi=nama_divisi,
        )
    )
