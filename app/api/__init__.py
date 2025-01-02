from fastapi import APIRouter

from app.api.auth.login import auth_login
from app.api.auth.register import authRegist
from app.api.auth.auth_refresh_token import auth_refresh_token
from app.api.auth.auth_logout import auth_logout
from app.api.auth.get_profile import get_profile, GetProfileResponseModel
from app.api.auth.edit_profile import edit_profile
from app.api.karyawan.add_karyawan import karyawan_add
from app.api.karyawan.edit_karyawan import edit_karyawan
from app.api.karyawan.get_karyawans import get_karyawans, GetDataKaryawansResponseModel
from app.api.rencana_kerja.get_rencana_kerjas import get_rencana_kerjas
from app.api.target.add_target import target_add
from app.api.target.update_target import update_target
from app.api.target.delete_target import delete_target
from app.api.target.get_targets import get_targets, GetDataTargetsResponseModel
from app.api.target.get_target import get_target, GetDataTargetResponseModel
from app.api.target.update_file_target import (
    upload_report_target,
    UploadReportTargetResponseModel,
)
from app.api.rencana_kerja.add_rencana_kerja import rencana_kerja_add
from app.api.rencana_kerja.delete_rencana_kerja import delete_rencana_kerja
from app.api.rencana_kerja.get_rencana_kerja import (
    get_rencana_kerja,
    GetRencanaKerjaDataResponseModel,
)
from app.api.rencana_kerja.get_rencana_kerjas import (
    get_rencana_kerjas,
    GetDataRencanaKerjasResponseModel,
)
from app.api.rencana_kerja.update_rencana_kerja import update_rencana_kerja
from app.api.rencana_kerja.update_file_rencana_kerja import (
    upload_report_rencana_kerja,
    UploadReportRencanaKerjaResponseModel,
)
from app.api.tugas.add_tugas import tugas_add
from app.api.tugas.delete_tugas import delete_tugas
from app.api.tugas.get_tugas import get_tugas
from app.api.tugas.get_tugases import get_tugases
from app.api.tugas.update_file_tugas import upload_report_tugas, UploadPpResponseModel
from app.api.tugas.update_tugas import update_tugas
from app.api.divisi.get_divisies import get_divisies, GetDataDivisiesResponseModel
from app.api.divisi.get_divisi import get_divisi, GetDivisiDataResponseModel
from app.api.catatan_tugas.add_catatan_tugas import add_catatan_tugas
from app.api.catatan_tugas.get_catatan_tugas import (
    get_catatan_tugas,
    GetDataCatatanTugasResponseModel,
)
from app.api.catatan_tugas.get_catatan_tugases import (
    get_catatan_tugases,
    GetDataCatatanTugasesResponseModel,
)
from app.api.catatan_renker.get_catatan_renker import (
    get_catatan_renker,
    GetDataCatatanRenkerResponseModel,
)
from app.api.catatan_renker.get_catatan_renkers import (
    get_catatan_renkers,
    GetDataCatatanRenkeresResponseModel,
)
from app.api.catatan_renker.add_catatan_renker import add_catatan_renker
from app.api.catatan_target.add_catatan_target import add_catatan_target
from app.api.catatan_target.get_catatan_target import (
    get_catatan_target,
    GetDataCatatanTargetResponseModel,
)
from app.api.catatan_target.get_catatan_targets import (
    get_catatan_targets,
    GetDataCatatanTargetsResponseModel,
)
from app.api.divisi.get_file_report import get_file_report

# from app.api.notification.add_token_notification import add_notification
from app.api.push_notification.token_notification import save_firebase_token
from app.api.notification.get_notification import (
    get_notifications,
    get_unread_notifications_count,
)
from app.api.notification.read_notification import mark_notification_read
from app.api.notification.websocket_notification import websocket_endpoint


api_router = APIRouter(prefix="/api")


# TWebSocket route
api_router.add_websocket_route("/ws/notifications", websocket_endpoint)

# AUTH
api_router.add_api_route(
    "/api/v1/auth/register",
    authRegist,
    methods=["POST"],
    tags=["Auth"],
    status_code=201,
)

api_router.add_api_route(
    "/api/v1/auth/login", auth_login, methods=["POST"], tags=["Auth"], status_code=201
)

api_router.add_api_route(
    "/api/v1/auth/refresh_token",
    auth_refresh_token,
    methods=["POST"],
    tags=["Auth"],
    status_code=201,
)

api_router.add_api_route(
    "/api/v1/auth/logout", auth_logout, methods=["POST"], tags=["Auth"], status_code=201
)

api_router.add_api_route(
    "/api/v1/auth/get_profile",
    get_profile,
    methods=["GET"],
    tags=["Auth"],
    response_model=GetProfileResponseModel,
)

api_router.add_api_route(
    "/api/v1/auth/edit_profile",
    edit_profile,
    methods=["POST"],
    tags=["Auth"],
    status_code=201,
)

# NOTIFIKASI
# api_router.add_api_route('/api/v1/notification',check_token,
#                         methods=['GET'], tags=['Notification'], status_code=200)
# api_router.add_api_route('/api/v1/notification',add_notification,
#                         methods=['POST'], tags=['Notification'], status_code=201)
api_router.add_api_route(
    "/api/v1/notifications",
    get_notifications,
    methods=["GET"],
    tags=["Notification"],
    status_code=200,
)
api_router.add_api_route(
    "/api/v1/unread_notifications",
    get_unread_notifications_count,
    methods=["GET"],
    tags=["Notification"],
    status_code=200,
)
api_router.add_api_route(
    "/api/v1/mark_notification",
    mark_notification_read,
    methods=["POST"],
    tags=["Notification"],
    status_code=201,
)
api_router.add_api_route(
    "/api/v1/save_firebase_token",
    save_firebase_token,
    methods=["POST"],
    tags=["Notification"],
    status_code=201,
)


# KARYAWAN
api_router.add_api_route(
    "/api/v1/karyawan/karyawan_add",
    karyawan_add,
    methods=["POST"],
    tags=["karyawan"],
    status_code=201,
)

api_router.add_api_route(
    "/api/v1/karyawan/edit_karyawan",
    edit_karyawan,
    methods=["POST"],
    tags=["karyawan"],
    status_code=201,
)

api_router.add_api_route(
    "/api/v1/karyawan/get_karyawans",
    get_karyawans,
    methods=["POST"],
    tags=["karyawan"],
    response_model=GetDataKaryawansResponseModel,
)

# TARGET
api_router.add_api_route(
    "/api/v1/target/add_target",
    target_add,
    methods=["POST"],
    tags=["target"],
    status_code=201,
)

api_router.add_api_route(
    "/api/v1/target/update_target",
    update_target,
    methods=["POST"],
    tags=["target"],
    status_code=201,
)

api_router.add_api_route(
    "/api/v1/target/delete_target",
    delete_target,
    methods=["POST"],
    tags=["target"],
    status_code=201,
)

api_router.add_api_route(
    "/api/v1/target/get_targets",
    get_targets,
    methods=["POST"],
    tags=["target"],
    response_model=GetDataTargetsResponseModel,
)

api_router.add_api_route(
    "/api/v1/target/get_target",
    get_target,
    methods=["POST"],
    tags=["target"],
    response_model=GetDataTargetResponseModel,
)

api_router.add_api_route(
    "/api/v1/target/upload_file_target",
    upload_report_target,
    methods=["POST"],
    tags=["target"],
    response_model=UploadReportTargetResponseModel,
)

# RENCANA KERJA
api_router.add_api_route(
    "/api/v1/rencana_kerja/add_rencana_kerja",
    rencana_kerja_add,
    methods=["POST"],
    tags=["rencanaKerja"],
    status_code=201,
)

api_router.add_api_route(
    "/api/v1/rencana_kerja/dellete_rencana_kerja",
    delete_rencana_kerja,
    methods=["POST"],
    tags=["rencanaKerja"],
    status_code=201,
)

api_router.add_api_route(
    "/api/v1/rencana_kerja/get_rencana_kerja",
    get_rencana_kerja,
    methods=["POST"],
    tags=["rencanaKerja"],
    response_model=GetRencanaKerjaDataResponseModel,
)

api_router.add_api_route(
    "/api/v1/rencana_kerja/get_rencana_kerjas",
    get_rencana_kerjas,
    methods=["POST"],
    tags=["rencanaKerja"],
    response_model=GetDataRencanaKerjasResponseModel,
)

api_router.add_api_route(
    "/api/v1/rencana_kerja/update_rencana_kerja",
    update_rencana_kerja,
    methods=["POST"],
    tags=["rencanaKerja"],
    status_code=201,
)

api_router.add_api_route(
    "/api/v1/rencana_kerja/upload_file_rencana_kerja",
    upload_report_rencana_kerja,
    methods=["POST"],
    tags=["rencanaKerja"],
    response_model=UploadReportRencanaKerjaResponseModel,
)


# TUGAS
api_router.add_api_route(
    "/api/v1/tugas/add_tugas",
    tugas_add,
    methods=["POST"],
    tags=["tugas"],
    status_code=201,
)

api_router.add_api_route(
    "/api/v1/tugas/delete_tugas",
    delete_tugas,
    methods=["POST"],
    tags=["tugas"],
    status_code=201,
)

api_router.add_api_route(
    "/api/v1/tugas/get_tugas",
    get_tugas,
    methods=["POST"],
    tags=["tugas"],
    status_code=201,
)

api_router.add_api_route(
    "/api/v1/tugas/get_tugases",
    get_tugases,
    methods=["POST"],
    tags=["tugas"],
    status_code=201,
)

api_router.add_api_route(
    "/api/v1/tugas/upload_file_tugas",
    upload_report_tugas,
    methods=["POST"],
    tags=["tugas"],
    response_model=UploadPpResponseModel,
)

api_router.add_api_route(
    "/api/v1/tugas/update_tugas",
    update_tugas,
    methods=["POST"],
    tags=["tugas"],
    status_code=200,
)

# DIVISI
api_router.add_api_route(
    "/api/v1/divisi/get_divisies",
    get_divisies,
    methods=["GET"],
    tags=["divisi"],
    response_model=GetDataDivisiesResponseModel,
)

api_router.add_api_route(
    "/api/v1/divisi/get_divisi",
    get_divisi,
    methods=["POST"],
    tags=["divisi"],
    response_model=GetDivisiDataResponseModel,
)

api_router.add_api_route(
    "/api/v1/divisi/report", get_file_report, methods=["GET"], tags=["divisi"]
)


# catatan_tugas
api_router.add_api_route(
    "/api/v1/catatan_tugas/add_catatan_tugas",
    add_catatan_tugas,
    methods=["POST"],
    tags=["catatan_tugas"],
    status_code=200,
)

api_router.add_api_route(
    "/api/v1/catatan_tugas/get_catatan_tugas",
    get_catatan_tugas,
    methods=["POST"],
    tags=["catatan_tugas"],
    response_model=GetDataCatatanTugasResponseModel,
)

api_router.add_api_route(
    "/api/v1/catatan_tugas/get_catatan_tugases",
    get_catatan_tugases,
    methods=["POST"],
    tags=["catatan_tugas"],
    response_model=GetDataCatatanTugasesResponseModel,
)

# catatan_renker
api_router.add_api_route(
    "/api/v1/catatan_renker/add_catatan_renker",
    add_catatan_renker,
    methods=["POST"],
    tags=["catatan_renker"],
    status_code=200,
)

api_router.add_api_route(
    "/api/v1/catatan_renker/get_catatan_renker",
    get_catatan_renker,
    methods=["POST"],
    tags=["catatan_renker"],
    response_model=GetDataCatatanRenkerResponseModel,
)


api_router.add_api_route(
    "/api/v1/catatan_renker/get_catatan_renkers",
    get_catatan_renkers,
    methods=["POST"],
    tags=["catatan_renker"],
    response_model=GetDataCatatanRenkeresResponseModel,
)

# catatan_target
api_router.add_api_route(
    "/api/v1/catatan_target/add_catatan_target",
    add_catatan_target,
    methods=["POST"],
    tags=["catatan_target"],
    status_code=200,
)

api_router.add_api_route(
    "/api/v1/catatan_target/get_catatan_target",
    get_catatan_target,
    methods=["POST"],
    tags=["catatan_target"],
    response_model=GetDataCatatanTargetResponseModel,
)

api_router.add_api_route(
    "/api/v1/catatan_targets/get_catatan_targets",
    get_catatan_targets,
    methods=["POST"],
    tags=["catatan_target"],
    response_model=GetDataCatatanTargetsResponseModel,
)
