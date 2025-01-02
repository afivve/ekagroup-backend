import time
from typing import Tuple

import jwt

from app.config import config


def generate_refresh_token(payload: str) -> str:
    current_time = int(time.time())

    payload.update({  # type: ignore
        'iat': current_time
    })

    # print('|' , config.REFRESHPRIVATEKEY.encode('utf-8'))

    refresh_tokenc = jwt.encode(
        payload, config.REFRESHPRIVATEKEY.encode('utf-8'),'RS256')  # type: ignore

    return refresh_tokenc
