from datetime import datetime
from typing import List
from pydantic import BaseModel
from app.api_models.profile_model import ProfileModel


class TugasModel(BaseModel):
    id_renker: int
    id_tugas: int
    judul: str
    kpi: str
    deskripsi: str
    start_date: datetime
    modified_at: datetime | None
    deadline: datetime
    catatan: str | None
    file_name: str | None
    id_divisi: int
    status: int
    id_karyawan: str
    progres: int
    prioritas: int | None
    pelaksana: str
    nama_divisi: str

    class Config:
        from_attributes = True
