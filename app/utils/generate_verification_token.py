
import time
from typing import Tuple

import jwt

from app.config import config


def generate_verification_token(payload: str) -> Tuple[str, int]:
    current_time = int(time.time())
    expired_at = current_time + config.VERIFICATION_EXPIRATION

    payload.update({  # type: ignore
        'exp': expired_at,
        'iat': current_time
    })

    access_token = jwt.encode(
        payload, config.PRIVATEKEY.encode('utf-8'), 'RS256')  # type: ignore
    print('expayetttttt', config.VERIFICATION_EXPIRATION)
    return access_token, config.VERIFICATION_EXPIRATION * 1000
