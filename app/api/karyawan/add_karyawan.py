from fastapi import Depends, HTTPException, Response, status
import sqlalchemy as sa
from pydantic import BaseModel
from app.models.user import User
from app.dependencies.get_db_session import get_db_session


class AddKaryawantData(BaseModel):
    id_karyawan: str
    nik: str
    full_name: str
    alamat: str
    jenis_kelamin: str
    divisi: int
    jabatan: int
    access: int


async def karyawan_add(data: AddKaryawantData, session=Depends(get_db_session)):
    try:
        # Check if the NIK already exists in the database
        nik_exists = session.execute(
            sa.select(User.nik).where(User.nik == data.nik)
        ).scalar()

        if nik_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="NIK is already registered",
            )

        # Check if the ID Karyawan already exists in the database
        id_karyawan_exists = session.execute(
            sa.select(User.id_karyawan).where(User.id_karyawan == data.id_karyawan)
        ).scalar()

        if id_karyawan_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID Karyawan is already registered",
            )

        # Create new user
        user = User(
            id_karyawan=data.id_karyawan,
            nik=data.nik,
            full_name=data.full_name,
            alamat=data.alamat,
            jenis_kelamin=data.jenis_kelamin,
            divisi=data.divisi,
            jabatan=data.jabatan,
            access=data.access,
        )

        # Add the user to the session and commit the transaction
        session.add(user)
        session.commit()

        # Return a success response
        return Response(
            content="Karyawan added successfully", status_code=status.HTTP_201_CREATED
        )

    except Exception as e:
        # Rollback the session in case of any error
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
