from typing import List
from jose import jwt, JWTError
from pydantic import BaseModel
from app.models.jwtToken import Token as jwtToken
import os
from datetime import datetime, timedelta
from typing import Union, Any
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.exceptions import UnauthorizedException, CredentialsException
from app.schemas.userSchemas import UserSchema
from app.models.User import User
from app.models.jwtToken import Token
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 # 60 minutes

JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']   # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']    # should be kept secret
ALGORITHM = "HS256"

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True, allowed_roles: list[str] = None,  allowed_permissions: list[str] = None):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.allowed_roles = allowed_roles
        self.allowed_permissions = allowed_permissions


    async def __call__(self, request: Request, db: Session = Depends(get_db)) -> str:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            self.delete_expired_tokens(db)
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Jeton d'authentification invalide.")
            
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Jeton d'authentification expiré ou invalide.")
            
            username : str = decode_token(credentials.credentials)
            if username is None:
                raise UnauthorizedException()
            
            current_user: UserSchema = db.query(User).filter(User.username == username).first()
            if current_user is None:
                raise UnauthorizedException()
            
            if self.allowed_permissions is not None and not user_has_permission(current_user=current_user, permission_codes=self.allowed_permissions):
                raise HTTPException(status_code=403, detail="Opération interdite.")
            
            elif self.allowed_roles is not None and not self.has_role(current_user):
                raise HTTPException(status_code=403, detail="Opération interdite.")
                
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Code d'authorisation invalide.")
        

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = decode_token(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
    

    def delete_expired_tokens(self, db: Session):
        """
        Supprime les tokens expirés
        
        Parameters
        ----------
        db: Manages persistence for ORM-Mapped object.
        """
        expired_date = datetime.utcnow()
        expired_tokens = Token.__table__.delete().where(Token.expires_in < expired_date)
        db.execute(expired_tokens)
        db.commit()


    def has_role(self, user):
        """
        Détecte si l'utilisateur fait partie d'un groupe
        
        Parameters
        ----------
        user: Utilisateur authentifié.
        """
        for group in user.groups:
            if group.name not in self.allowed_roles:
                return False
        return True


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    """
    Créer un token d'accès pour l'utilisateur.

    Parameters
    ----------
    subject: Paramètre à encoder dans le token (username).
    expires_delta: Délais d'expiration du token.
    """
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": int(expires_delta.timestamp()), "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    """
    Créer le token de rafraîchissement de l'utilisateur.

    Parameters
    ----------
    subject: Paramètre à encoder dans le token (username).
    expires_delta: Délais d'expiration du token.
    """
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": int(expires_delta.timestamp()), "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def decode_token(token):
    """
    Decode le token, évalue s'il est expiré et retourne le username si valide.

    Parameters
    ----------
    token: jwt token d'authentification.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
        expires_at = payload.get("exp")
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException()
        if expires_at < datetime.utcnow().timestamp():
            print(expires_at)
            print( datetime.utcnow().timestamp())
            raise HTTPException(status_code=400, details="Token is expired")
    except JWTError as e:
        raise CredentialsException()
    return username


def refresh_token(token: jwtToken):
    """
    Raffraichis le token s'il est valide.

    Parameters
    ----------
    refresh_token: Token de rafraichissement.
    """
    try:
        payload = jwt.decode(token.refresh_token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        expires_at = payload.get("exp")
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException()
        if expires_at < datetime.utcnow().timestamp():
            return
    except JWTError:
        raise CredentialsException()
    jwt_token = create_access_token(username)
    jwt_refresh_token = create_refresh_token(username)
    expires = jwt.decode(jwt_token, JWT_SECRET_KEY, algorithms=[ALGORITHM]).get("exp")
    new_db_token = Token(user_id = token.user_id, access_token = jwt_token, refresh_token = jwt_refresh_token, expires_in = datetime.utcnow() + timedelta(minutes=expires))
    return new_db_token


def user_has_permission(current_user: UserSchema, group_names: list[str], permission_codes : list[str]) -> bool | UnauthorizedException:
        """
        Évalue si l'utilisateur à les permissions nécessaires.
        Retourne True si l'utilisateur à les permissions nécessaires pour accéder au contenu.

        Parameters
        ----------
        current_user: utilisateur authentifié.
        permission_code: code de permission.
        """
        for group in current_user.groups:
            if "Admin" in group.name:
                # bypass permissions if user is admin as admins has all permissions.
                return {"has_permission": True}
            for permission in group.permissions:
                if permission.code in permission_codes and permission.group_name in group_names:
                    return {"has_permission": True}
        raise UnauthorizedException()