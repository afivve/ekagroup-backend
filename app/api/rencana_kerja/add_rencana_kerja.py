from fastapi import Depends, HTTPException, Response, status
import sqlalchemy as sa
from pydantic import BaseModel
from app.dependencies.autentication import Autentication
from app.models.rencana_kerja import RencanaKerja
from app.models.target import Target
from app.dependencies.get_db_session import get_db_session
from app.dependencies.str_to_date import str_to_date


class AddRencanaKerjaData(BaseModel):
    judul: str
    deskripsi: str
    kpi: str
    start_date: str
    deadline: str
    id_target: int


async def rencana_kerja_add(
    data: AddRencanaKerjaData,
    payload=Depends(Autentication()),
    session=Depends(get_db_session),
):

    # Commit the transaction
    try:
        # Check if the title already exists
        judul_exists = session.execute(
            sa.select(RencanaKerja.judul).where(RencanaKerja.judul == data.judul)
        ).scalar()

        if judul_exists:
            raise HTTPException(
                status_code=400, detail="The title is already registered."
            )

        # Get the division ID based on the target ID
        id_divisi = session.execute(
            sa.select(Target.id_divisi).where(Target.id_target == data.id_target)
        ).scalar()

        if not id_divisi:
            raise HTTPException(
                status_code=404, detail="Target not found for the given ID."
            )

        # Create new RencanaKerja entry
        rencana_kerja = RencanaKerja(
            judul=data.judul,
            deskripsi=data.deskripsi,
            kpi=data.kpi,
            start_date=str_to_date(data.start_date),
            deadline=str_to_date(data.deadline),
            id_divisi=id_divisi,
            id_target=data.id_target,
        )

        # Add the new entry to the session
        session.add(rencana_kerja)

        session.commit()
    except Exception as e:
        session.rollback()  # Rollback in case of error
        print(f"Error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )

    return Response(status_code=201)  # Created status code
