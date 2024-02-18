from pydantic import BaseModel
from datetime import datetime


class Token(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: datetime
    token_type: str = 'Bearer'


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []

class jwtTokenSchema(BaseModel):
    token: Token
    password_expired: bool | None = False