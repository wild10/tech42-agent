import time
import requests
from jose import jwk, jwt
from jose.utils import base64url_decode
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.core.config import COGNITO_REGION, COGNITO_USER_POOL_ID, COGNITO_APP_CLIENT_ID

security = HTTPBearer()

# JWKS cache
_jwks_cache = None
_jwks_last_fetch = 0

def get_jwks():
    global _jwks_cache, _jwks_last_fetch
    now = time.time()
    if _jwks_cache is None or now - _jwks_last_fetch > 3600:
        url = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"
        response = requests.get(url)
        response.raise_for_status()
        _jwks_cache = response.json()["keys"]
        _jwks_last_fetch = now
    return _jwks_cache

async def get_current_user(auth: HTTPAuthorizationCredentials = Depends(security)):
    token = auth.credentials
    try:
        # Get headers to find the kid
        headers = jwt.get_unverified_headers(token)
        kid = headers.get("kid")
        if not kid:
            raise HTTPException(status_code=401, detail="Missing kid in token headers")

        # Find the public key
        keys = get_jwks()
        key_index = -1
        for i in range(len(keys)):
            if kid == keys[i]["kid"]:
                key_index = i
                break
        if key_index == -1:
            raise HTTPException(status_code=401, detail="Public key not found in JWKS")

        # Construct the public key
        public_key = jwk.construct(keys[key_index])

        # Verify the signature
        message, encoded_signature = str(token).rsplit(".", 1)
        decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
        if not public_key.verify(message.encode("utf8"), decoded_signature):
            raise HTTPException(status_code=401, detail="Signature verification failed")

        # Verify claims
        claims = jwt.get_unverified_claims(token)
        
        # Check expiration
        if time.time() > claims["exp"]:
            raise HTTPException(status_code=401, detail="Token has expired")
        
        # Check audience (aud or client_id)
        if claims.get("client_id") != COGNITO_APP_CLIENT_ID and claims.get("aud") != COGNITO_APP_CLIENT_ID:
             raise HTTPException(status_code=401, detail="Token audience/client_id mismatch")
        
        # Check issuer
        expected_iss = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"
        if claims["iss"] != expected_iss:
            raise HTTPException(status_code=401, detail="Invalid token issuer")

        return claims
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")