from datetime import datetime
from typing import List
from pydantic import BaseModel


class ProfileModel(BaseModel):
    id_karyawan: str
    username: str
    full_name: str
    email: str|None
    noWa: str
    access: int
    path_foto: str
    nik: str
    alamat: str
    divisi: int
    jabatan: str
    nama_divisi: str
