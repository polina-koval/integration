import hmac
import hashlib
from functools import lru_cache

from starlette.requests import Request

from integration.errors.exceptions import AuthorizationError
from integration.app.config import settings


class HMACSHA256SignatureCheck:
    @lru_cache(1)
    def _get_secret(self) -> bytes:
        secret = settings.SERVICE_SECRET
        return secret.encode("ASCII")

    async def __call__(self, request: Request):
        secret = self._get_secret()
        if not secret:
            return
        body = await request.body()
        signature = hmac.new(secret, body, hashlib.sha256).hexdigest()
        given_signature = request.headers.get("X-API-Signature", "")
        if signature != given_signature:
            raise AuthorizationError()


hf_hooks_auth = HMACSHA256SignatureCheck()
