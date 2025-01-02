from pydantic import BaseModel
from typing import List, Optional
from app.api_models.profile_model import ProfileModel
from app.api_models.target_model import TargetModel
from app.api_models.rencana_kerja_model import RencanaKerjaModel
from app.api_models.tugas_model import TugasModel


class DivisiModel(BaseModel):
    id_divisi: int
    nama_divisi: str
    path_foto: Optional[str]
    jml_karyawan: int
    manager: Optional[ProfileModel] = None
    targets: List[TargetModel] = []  # Relasi ke Target
    rencana_kerja: List[RencanaKerjaModel] = []  # Relasi ke Rencana Kerja
    tugas: List[TugasModel] = []  # Relasi ke Tugas

    class Config:
        from_attributes = True  # Agar bisa menerima data dari objek ORM SQLAlchemy
