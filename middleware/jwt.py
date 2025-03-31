from fastapi import Request, HTTPException

SECRET_KEY = "mysecret"

async def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Требуется токен")

    token = auth_header.split(" ")[1]

    if token != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Невалидный токен")
