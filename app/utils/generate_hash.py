
import time
from typing import Tuple

import jwt

from app.config import config


def generate_hash(payload: str) -> str:
    current_time = int(time.time())
    expired_at = current_time + config.ACCESS_TOKEN_EXPIRATION

    payload.update({  # type: ignore
        'exp': expired_at,
        'iat': current_time
    })

    access_token = jwt.encode(
        payload, config.KEY_PRIVATE.encode('utf-8'), 'RS256')  # type: ignore

    return access_token
