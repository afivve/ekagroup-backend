from typing import Optional
from fastapi import Depends, HTTPException, Response
import sqlalchemy as sa
from pydantic import BaseModel
from app.dependencies.autentication import Autentication
from app.models.rencana_kerja import RencanaKerja
from app.dependencies.get_db_session import get_db_session
from app.models.user import User


class DeleteRencanaKerjaData(BaseModel):
    id_rencana_kerja: int


async def delete_rencana_kerja(
    data: DeleteRencanaKerjaData,
    payload=Depends(Autentication()),
    session=Depends(get_db_session),
):
    try:
        # Check user access
        id_strong_user = payload.get("uid", 0)

        user_access = session.execute(
            sa.select(User.access).where(User.id_karyawan == id_strong_user)
        ).scalar()

        if user_access < 3:
            raise HTTPException(
                status_code=403,
                detail="You do not have sufficient access rights to delete.",
            )

        # Check if the Rencana Kerja exists
        id_exists = session.execute(
            sa.select(RencanaKerja.id_renker).where(
                RencanaKerja.id_renker == data.id_rencana_kerja
            )
        ).scalar()

        if not id_exists:
            raise HTTPException(status_code=404, detail="Rencana Kerja not found.")

        # Perform the delete operation
        result = session.execute(
            sa.delete(RencanaKerja).where(
                RencanaKerja.id_renker == data.id_rencana_kerja
            )
        )

        # If no rows were deleted, raise an error
        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Rencana Kerja could not be deleted as it was not found.",
            )

        # Commit the transaction
        session.commit()

        return Response(status_code=204)  # No Content

    except HTTPException as e:
        # Handle known HTTP exceptions
        raise e

    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
