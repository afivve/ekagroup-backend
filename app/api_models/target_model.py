from datetime import datetime
from typing import List
from pydantic import BaseModel


class TargetModel(BaseModel):
    id_target: int
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
    progres: int
    prioritas: int
    nama_divisi: str

    class Config:
        from_attributes = True
