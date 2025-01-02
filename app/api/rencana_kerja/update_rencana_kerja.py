# from typing import Optional
# from fastapi import Depends,HTTPException,Response
# from fastapi.encoders import jsonable_encoder
# import sqlalchemy as sa
# from pydantic import BaseModel, model_validator
# import datetime
# from app.dependencies.autentication import Autentication

# from app.models.rencana_kerja import RencanaKerja
# from app.dependencies.get_db_session import get_db_session
# from app.dependencies.str_to_date import str_to_date
# from app.models.user import User

# class UpdateRencanaKerjaData(BaseModel):
#     id_renker:int
#     id_divisi:Optional[int]
#     judul:Optional[str] = None
#     deskripsi :Optional[str] = None
#     kpi: Optional[str] = None
#     deadline: Optional[str] = None
#     catatan : Optional[str] = None
#     progres : Optional[int] = None
#     status : Optional[int] = None
#     file_name : Optional[str] = None


# async def update_rencana_kerja(data:UpdateRencanaKerjaData,payload=Depends(Autentication()),session=Depends(get_db_session)):

#     user_id = payload.get('uid', 0)
#     user_data = session.execute(sa.select(User.access,User.divisi).where(User.id_karyawan == user_id)).fetchone()

#     #  jika akses  ==0 maka akses ditolak
#     if  user_data.access == 0 :
#         raise HTTPException(400, detail='User not have access')
#     #  jika akses < 3 maka sql dibatasi di divisi nya saja
#     elif user_data.access < 3:
#         if data.id_divisi != user_data.divisi :
#              raise HTTPException(400, detail=f'User not have access {data.id_divisi}')
#     elif user_data.access > 3 :
#         pass
#     else : raise HTTPException(400, detail=" anda tidak mmemiliki akses ")


#     # cek id tersedia
#     id_exis = session.execute(
#         sa.select(RencanaKerja.id_renker).where(RencanaKerja.id_renker == data.id_renker)
#         ).scalar()
#     # print(id_exis)

#     if not id_exis :
#         raise HTTPException(
#             400, detail='Rencana kerja yang dimaksud tidak tersedia')


#     judul_exis = session.execute(
#     sa.select(RencanaKerja.judul).where(RencanaKerja.judul == data.judul)
#     ).scalar()

#     # cek nik tersedia
#     if judul_exis :
#         raise HTTPException(
#             400, detail='judul sudah terdaftar')

#     target_data = jsonable_encoder(data)
#     # TODO:
#     values_to_update = {}

#     if 'judul' in target_data and target_data['judul']:
#         values_to_update.update({'judul': target_data['judul']})

#     if 'deskripsi' in target_data and target_data['deskripsi']:
#         values_to_update.update({'deskripsi': target_data['deskripsi']})

#     if 'kpi' in target_data and target_data['kpi']:
#         values_to_update.update({'kpi': target_data['kpi']})

#     if 'deadline' in target_data and target_data['deadline']:
#         values_to_update.update({'deadline':str_to_date(data.deadline) })

#     if 'catatan' in target_data and target_data['catatan']:
#         values_to_update.update({'catatan': target_data['catatan']})

#     if 'progres' in target_data and target_data['progres']:
#         values_to_update.update({'progres': target_data['progres']})

#     if 'status' in target_data and target_data['status']:
#         values_to_update.update({'status': target_data['status']})

#     if 'file_name' in target_data and target_data['file_name']:
#         values_to_update.update({'file_name': target_data['file_name']})

#     result = session.execute(
#         sa.update(RencanaKerja).values(**values_to_update).where(RencanaKerja.id_renker == data.id_renker)
#     )

#     if result.rowcount == 0:
#         raise HTTPException(400, detail='Target not found')


#     session.commit()

#     return

from typing import Optional
from fastapi import Depends, HTTPException, Response
from fastapi.encoders import jsonable_encoder
import sqlalchemy as sa
from pydantic import BaseModel
from app.dependencies.autentication import Autentication
from app.models.rencana_kerja import RencanaKerja
from app.dependencies.get_db_session import get_db_session
from app.dependencies.str_to_date import str_to_date
from app.models.user import User


class UpdateRencanaKerjaData(BaseModel):
    id_renker: int
    id_divisi: Optional[int]
    judul: Optional[str] = None
    deskripsi: Optional[str] = None
    kpi: Optional[str] = None
    deadline: Optional[str] = None
    catatan: Optional[str] = None
    progres: Optional[int] = None
    status: Optional[int] = None
    file_name: Optional[str] = None


async def update_rencana_kerja(
    data: UpdateRencanaKerjaData,
    payload=Depends(Autentication()),
    session=Depends(get_db_session),
):
    try:
        user_id = payload.get("uid", 0)
        user_data = session.execute(
            sa.select(User.access, User.divisi).where(User.id_karyawan == user_id)
        ).fetchone()

        # Cek akses user
        if user_data.access == 0:
            raise HTTPException(400, detail="User tidak memiliki akses")

        # Batasi akses berdasarkan divisi jika akses < 3
        if user_data.access < 3 and data.id_divisi != user_data.divisi:
            raise HTTPException(
                400, detail=f"User tidak memiliki akses ke divisi {data.id_divisi}"
            )

        # Cek apakah rencana kerja tersedia
        id_exis = session.execute(
            sa.select(RencanaKerja.id_renker).where(
                RencanaKerja.id_renker == data.id_renker
            )
        ).scalar()

        if not id_exis:
            raise HTTPException(400, detail="Rencana kerja tidak ditemukan")

        # Cek apakah judul sudah ada
        if data.judul:
            judul_exis = session.execute(
                sa.select(RencanaKerja.judul).where(RencanaKerja.judul == data.judul)
            ).scalar()
            if judul_exis:
                raise HTTPException(400, detail="Judul sudah terdaftar")

        # Menyiapkan data untuk diperbarui
        values_to_update = {}
        if data.judul:
            values_to_update["judul"] = data.judul
        if data.deskripsi:
            values_to_update["deskripsi"] = data.deskripsi
        if data.kpi:
            values_to_update["kpi"] = data.kpi
        if data.deadline:
            values_to_update["deadline"] = str_to_date(data.deadline)
        if data.catatan:
            values_to_update["catatan"] = data.catatan
        if data.progres:
            values_to_update["progres"] = data.progres
        if data.status:
            values_to_update["status"] = data.status
        if data.file_name:
            values_to_update["file_name"] = data.file_name

        # Eksekusi update
        result = session.execute(
            sa.update(RencanaKerja)
            .values(**values_to_update)
            .where(RencanaKerja.id_renker == data.id_renker)
        )

        if result.rowcount == 0:
            raise HTTPException(400, detail="Rencana kerja gagal diperbarui")

        session.commit()

        return Response(status_code=204)

    except HTTPException as e:
        # Menangani HTTPException jika ada error yang dilempar
        raise e
    except Exception as e:
        # Menangani error tak terduga
        raise HTTPException(
            status_code=500,
            detail=f"Terjadi kesalahan saat memperbarui rencana kerja: {str(e)}",
        )
