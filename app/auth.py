from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
import os

apiKeyName = "onlinestore"
apiKey = os.getenv("apiKey")
if not apiKey:
    raise RuntimeError("API key not set in environment")
apiKeyHeader = APIKeyHeader(name= apiKeyName, auto_error=True)

async def get_apikey(api_key: str = Security(apiKeyHeader)):
    if api_key != apiKey:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key

