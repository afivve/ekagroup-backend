
from typing import Optional

import sqlalchemy as sa
from fastapi import Depends, HTTPException, Response
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel , model_validator
from werkzeug.security import generate_password_hash

from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.user import User


class EditProfileData(BaseModel):
    username: Optional[str] =None
    full_name: Optional[str] =None
    password: Optional[str] =None
    confirm_password: Optional[str] =None
    path_foto: Optional[str] =None
    email: Optional[str] =None
    noWa: Optional[str] =None
    nik: Optional[str] =None
    access: Optional[int] =None

    
    @model_validator(mode='before')
    def validate_confirm_password(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')

        if password and confirm_password != password:
            raise HTTPException(
                400, 'katasandi tidak sama ,ulangi dengan  benar !')

        return values


async def edit_profile(data: EditProfileData, payload=Depends(Autentication()), session=Depends(get_db_session)):
    profile_data = jsonable_encoder(data)
    user_id = payload.get('uid', 0)
    print(data,'idddd')


    # TODO:
    values_to_update = {}

    if 'username' in profile_data and profile_data['username']:
        # check username exist
        check_username = session.execute(
            sa.select(User.id_karyawan).where(
                sa.and_(
                    User.username == profile_data['username'],
                    User.id_karyawan != user_id
                )
            )
        ).fetchone()

        if check_username:
            raise HTTPException(400, 'Username telah digunakan akun lain')

        values_to_update.update({'username': profile_data['username']})

    if 'full_name' in profile_data and profile_data['full_name']:
        values_to_update.update({'full_name': profile_data['full_name']})

    if 'password' in profile_data and profile_data['password']:
        password = generate_password_hash(profile_data['password'])
        values_to_update.update({'password': password})

    if 'email' in profile_data and profile_data['email']:
        check_email = session.execute(
            sa.select(User.id_karyawan).where(
                sa.and_(
                    User.email == profile_data['email'],
                    User.id_karyawan != user_id
                )
            )
        ).fetchone()

        if check_email:
            raise HTTPException(400, 'email telah digunakan akun lain')
        values_to_update.update({'email': profile_data['email']})

    if 'noWa' in profile_data and profile_data['noWa']:
        check_noWa = session.execute(
            sa.select(User.id_karyawan).where(
                sa.and_(
                    User.noWa == profile_data['noWa'],
                    User.id_karyawan != user_id
                )
            )
        ).fetchone()

        if check_noWa:
            raise HTTPException(
                400, 'nomor whatsapp telah digunakan akun lain')
        values_to_update.update({'noWa': profile_data['noWa']})

    if 'path_foto' in profile_data and profile_data['path_foto']:
        values_to_update.update({'path_foto': profile_data['path_foto']})

    if 'nik' in profile_data and profile_data['nik']:
        # check username exist
        check_nik = session.execute(
            sa.select(User.id_karyawan).where(
                sa.and_(
                    User.nik == profile_data['nik'],
                    User.id_karyawan != user_id
                )
            )
        ).fetchone()

        if check_nik:
            raise HTTPException(400, 'Nik telah digunakan akun lain')

        values_to_update.update({'nik': profile_data['nik']})

    if 'alamat' in profile_data and profile_data['alamat']:
        values_to_update.update({'alamat': profile_data['alamat']})

    result = session.execute(
        sa.update(User).values(**values_to_update).where(User.id_karyawan == user_id)
    )

    if result.rowcount == 0:
        raise HTTPException(400, detail='User not found')

    session.commit()
    return Response(status_code=204)
