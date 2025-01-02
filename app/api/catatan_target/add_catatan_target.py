from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from app.dependencies.autentication import Autentication
from app.models.catatan_target import CatatanTarget
from app.dependencies.get_db_session import get_db_session


class AddCatatanTargetData(BaseModel):
    id_target: int
    catatan: str


async def add_catatan_target(
    data: AddCatatanTargetData,
    payload=Depends(Autentication()),
    session=Depends(get_db_session),
):
    try:
        # Membuat instance CatatanTarget
        catatan_target = CatatanTarget(
            id_target=data.id_target,
            catatan=data.catatan,
        )

        # Menyimpan ke database
        session.add(catatan_target)
        session.commit()

        return {"message": "Catatan berhasil ditambahkan"}

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
    finally:
        session.close()
