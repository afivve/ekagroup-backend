from typing import Optional
import sqlalchemy as sa
from fastapi import Depends, HTTPException, Response
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, model_validator
from app.dependencies.autentication import Autentication
from app.dependencies.get_db_session import get_db_session
from app.models.user import User


class EditKaryawanData(BaseModel):
    id_karyawan: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    noWa: Optional[str] = None
    nik: Optional[str] = None
    access: Optional[int] = None

    @model_validator(mode="before")
    def validate_confirm_password(cls, values):
        password = values.get("password")
        confirm_password = values.get("confirm_password")

        if password and confirm_password != password:
            raise HTTPException(
                status_code=400, detail="Passwords do not match. Please try again."
            )

        return values


async def edit_karyawan(
    data: EditKaryawanData,
    payload=Depends(Autentication()),
    session=Depends(get_db_session),
):
    # Get the authenticated user's id and access level
    id_strong_user = payload.get("uid", 0)

    # Check if the user has sufficient access to edit other users
    user_access = session.execute(
        sa.select(User.access).where(User.id_karyawan == id_strong_user)
    ).scalar()
    if user_access < 3:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this resource.",
        )

    # Convert the input data into a dictionary for processing
    profile_data = jsonable_encoder(data)
    user_id = data.id_karyawan

    # Initialize a dictionary to store values to be updated
    values_to_update = {}

    # Check and add fields to update
    if "full_name" in profile_data and profile_data["full_name"]:
        values_to_update["full_name"] = profile_data["full_name"]

    if "email" in profile_data and profile_data["email"]:
        check_email = session.execute(
            sa.select(User.id_karyawan).where(
                sa.and_(
                    User.email == profile_data["email"], User.id_karyawan != user_id
                )
            )
        ).scalar()

        if check_email:
            raise HTTPException(
                status_code=400,
                detail="The email is already associated with another account.",
            )
        values_to_update["email"] = profile_data["email"]

    if "noWa" in profile_data and profile_data["noWa"]:
        check_noWa = session.execute(
            sa.select(User.id_karyawan).where(
                sa.and_(User.noWa == profile_data["noWa"], User.id_karyawan != user_id)
            )
        ).scalar()

        if check_noWa:
            raise HTTPException(
                status_code=400,
                detail="The WhatsApp number is already associated with another account.",
            )
        values_to_update["noWa"] = profile_data["noWa"]

    if "alamat" in profile_data and profile_data["alamat"]:
        values_to_update["alamat"] = profile_data["alamat"]

    # Perform the update
    if not values_to_update:
        raise HTTPException(
            status_code=400, detail="No valid fields provided to update."
        )

    result = session.execute(
        sa.update(User).values(**values_to_update).where(User.id_karyawan == user_id)
    )

    # Check if the user was found and updated
    if result.rowcount == 0:
        raise HTTPException(
            status_code=404, detail="User not found or no changes were made."
        )

    # Commit the transaction
    session.commit()

    # Return a success response
    return Response(status_code=204)
