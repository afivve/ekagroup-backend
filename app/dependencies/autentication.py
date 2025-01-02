from typing import Optional
import sqlalchemy as sa
import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.dependencies.get_db_session import get_db_session
from app.utils.get_payload import get_payload
from app.models.user_login import UserLogin


class Autentication(HTTPBearer):
    async def __call__(self, request: Request,session=Depends(get_db_session)) -> Optional[HTTPAuthorizationCredentials]:
        authorization = await super().__call__(request)
        
        # cek login session di db
        # is_login = session.execute(sa.select(UserLogin.refresh_token).where(UserLogin.refresh_token == authorization.credentials)).scalar()
        # if not is_login:
        #     print(is_login, 'is loginn')

        # if not is_login:
        #     return {}
        if not authorization.credentials :
            return {}
        try:
            payload = get_payload(authorization.credentials)
        


        except jwt.ExpiredSignatureError:
            raise HTTPException(
                401,
                detail={
                    'message': 'Token expired',
                    'code': 40100
                }
            )

        except jwt.DecodeError:
            raise HTTPException(
                401,
                detail={
                    'message': 'Token infalid',
                    'code': 40101
                }
            )

        return payload  # type: ignore
