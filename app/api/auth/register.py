from fastapi import Depends,HTTPException,Response
import sqlalchemy as sa
from pydantic import BaseModel, model_validator

from app.models.user import User
from app.dependencies.get_db_session import get_db_session
from werkzeug.security import generate_password_hash



class RegistData(BaseModel):
    nik :str
    password: str
    confirm_password: str
    username: str

    # cek kecocokan password
    @model_validator(mode='before')
    def validate_confirm_password(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')

        if confirm_password != password:
            raise ValueError('Confirm password tidak cocok')

        return values

async def authRegist(data:RegistData,session=Depends(get_db_session)):
    # cek nik di db
    nik_exis = session.execute(
        sa.select(User.nik).where(User.nik == data.nik)
        ).scalar()

    # cek nik tersedia
    if  nik_exis :
        username_exis = session.execute(
            sa.select(User.username).where(User.nik == data.nik)
            ).scalar()
        if  username_exis:
            raise HTTPException(
            400, detail='nik telah terdaftar oleh akun lain')
    else:
        raise HTTPException(
            400, detail='nik belum tersedia')
    
    username_exis = session.execute(
        sa.select(User.username).where(User.username == data.username)
        ).scalar()

    # cek username tersedia
    if username_exis :
        raise HTTPException(
            400, detail='username telah digunakan akun lain')
    
    encripted_password = generate_password_hash(data.password)

    values_to_update = {
        'username':data.username.lower(),
        'password':encripted_password,
        'access':1
    }
    result = session.execute(
        sa.update(User).values(**values_to_update).where(User.nik == data.nik)
        )
    

    if result.rowcount == 0:
        raise HTTPException(400, detail='Karyawan tidak ditemukan')
    
    session.commit()
    return Response(status_code=201)


