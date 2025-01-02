# import datetime
# import sqlalchemy as sa
# from fastapi import Depends
# from fastapi.exceptions import HTTPException
# from pydantic import BaseModel

# from app.api_models import BaseResponseModel
# from app.config import config
# from app.dependencies.get_db_session import get_db_session
# from app.models.user import User
# from app.models.user_login import UserLogin
# from app.utils.generate_access_token import generate_access_token


# class RefreshTokenData(BaseModel):
#     refresh_token: str


# class RefreshTokenDataResponseModel(BaseModel):
#     access_token: str
#     expired_at: int


# class RefreshTokenResponseMode(BaseResponseModel):
#     data: RefreshTokenDataResponseModel

#     class Config:
#         json_schema_extra = {
#             'example': {
#                 'data': {
#                     'refresh_token': 'abc.def.ghi',
#                     'expired_at': 123456
#                 },
#                 'meta': {},
#                 'message': 'Success',
#                 'success': True,
#                 'code': 200
#             }
#         }


# async def auth_refresh_token(data: RefreshTokenData, session=Depends(get_db_session)):
#     # cek refresh token
#     user_login = session.execute(
#         sa.select(
#             UserLogin.id_karyawan,
#             User.id_karyawan.label('id_karyawan'),
#             User.username,
#             sa.func.if_(
#                 UserLogin.expired_at > sa.func.NOW(), 0, 1
#             ).label(
#                 'expired'
#             )
#         ).where(
#             UserLogin.id_karyawan == User.id_karyawan,
#             UserLogin.refresh_token == data.refresh_token
#         )
#     ).fetchone()

#     if not user_login:
#         raise HTTPException(status_code=400, detail='Reftesh token not found')

#     if user_login.expired:
#         print(user_login.expired,"expired")
#         raise HTTPException(status_code=403, detail={
#             'message': 'Reftesh token expaied',
#             'code': 40301
#         }
#         )
#     # extend expiration of refresh token
#     session.execute(
#         sa.update(
#             UserLogin
#         ).values(
#             expired_at=sa.func.TIMESTAMPADD(
#                 sa.text('SECOND'),
#                 config.REFRESH_TOKEN_EXPIRATION,
#                 datetime.datetime.now()
#             )
#         )
#     )

#     # generate acces token yang baru
#     payload = {
#         'uid': user_login.id_karyawan,
#         'username': user_login.username,
#     }
#     access_token, expired_at = generate_access_token(payload)  # type: ignore

#     session.commit()

#     return RefreshTokenResponseMode(
#         data=RefreshTokenDataResponseModel(
#             access_token=access_token,
#             expired_at=expired_at
#         )

#     )


import datetime
import sqlalchemy as sa
from fastapi import Depends, HTTPException
from pydantic import BaseModel

from app.api_models import BaseResponseModel
from app.config import config
from app.dependencies.get_db_session import get_db_session
from app.models.user import User
from app.models.user_login import UserLogin
from app.utils.generate_access_token import generate_access_token


# Request model for refresh token data
class RefreshTokenData(BaseModel):
    refresh_token: str


# Response model for new access token and its expiration
class RefreshTokenDataResponseModel(BaseModel):
    access_token: str
    expired_at: int


# Response model for the refresh token API response
class RefreshTokenResponseMode(BaseResponseModel):
    data: RefreshTokenDataResponseModel

    class Config:
        json_schema_extra = {
            "example": {
                "data": {"access_token": "new.access.token", "expired_at": 1234567890},
                "meta": {},
                "message": "Success",
                "success": True,
                "code": 200,
            }
        }


# Refresh token function to validate and issue new access token
async def auth_refresh_token(data: RefreshTokenData, session=Depends(get_db_session)):
    # Validate the provided refresh token
    try:
        user_login = session.execute(
            sa.select(
                UserLogin.id_karyawan,
                User.username,
                sa.func.if_(UserLogin.expired_at > sa.func.NOW(), 0, 1).label(
                    "expired"
                ),
            )
            .where(UserLogin.refresh_token == data.refresh_token)
            .join(User, User.id_karyawan == UserLogin.id_karyawan)
        ).fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    # If no matching refresh token found, raise an error
    if not user_login:
        raise HTTPException(status_code=400, detail="Refresh token not found")

    # If the refresh token has expired, raise an error
    if user_login.expired:
        raise HTTPException(
            status_code=403, detail={"message": "Refresh token expired", "code": 40301}
        )

    # Extend the expiration of the refresh token in the database
    try:
        session.execute(
            sa.update(UserLogin)
            .values(
                expired_at=sa.func.TIMESTAMPADD(
                    sa.text("SECOND"),
                    config.REFRESH_TOKEN_EXPIRATION,  # type: ignore
                    datetime.datetime.now(),
                )
            )
            .where(UserLogin.refresh_token == data.refresh_token)
        )
        session.commit()
    except Exception as e:
        session.rollback()  # Ensure rollback on error
        raise HTTPException(
            status_code=500, detail=f"Error updating refresh token expiration: {str(e)}"
        )

    # Generate a new access token
    payload = {
        "uid": user_login.id_karyawan,
        "username": user_login.username,
    }
    try:
        access_token, expired_at = generate_access_token(payload)  # type: ignore
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating access token: {str(e)}"
        )

    # Return the new access token and its expiration
    return RefreshTokenResponseMode(
        data=RefreshTokenDataResponseModel(
            access_token=access_token, expired_at=expired_at
        )
    )
