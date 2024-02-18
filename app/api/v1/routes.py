from fastapi import Depends, APIRouter, HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.exceptions import UnauthorizedException, IncorrectCredentialsException, CredentialsException
from app.db.session import get_db
from app.schemas.userSchemas import UpdateUserSchema, UpdateUserPasswordSchema, UserGetSchema
from app.schemas.jwtSchemas import jwtTokenSchema
from app.models.User import User
from app.models.jwtToken import Token

from app.utils.userUtils import get_current_user, create_user
from app.utils.passwordUtils import get_hashed_password, update_password_expired, verify_password, create_reset_link
from app.utils.jwtHandler import  create_access_token, create_refresh_token, user_has_permission, JWTBearer, refresh_token

router = APIRouter(
        prefix='/api/v1/',
        tags = ['/api/v1/'],
    )

jwtBearerScheme = JWTBearer()


@router.get("/current-user-is-admin", status_code=200)
async def current_user_is_admin(token: Annotated[str, Depends(jwtBearerScheme)], db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    for group in current_user.groups:
        if 'Admin' in group.name:
            return True
        else:
            raise UnauthorizedException()


@router.get("/current-user-has-permission/{group_name}/{permission_code}", description="Évalue si l'utilisateur à les permissions nécessaires pour accéder au contenu.", status_code=200)
async def current_user_has_permission(Token: Annotated[str, Depends(jwtBearerScheme)], permission_code: str, group_name: str, db: Session = Depends(get_db)):
    current_user = get_current_user(Token, db)
    return user_has_permission(current_user, [group_name], [permission_code])


@router.get("/profile/", description="Retourne l'utilisateur authentifié", response_model=UserGetSchema)
async def get_current_user_profile(token: Annotated[str, Depends(jwtBearerScheme)], db : Session = Depends(get_db)) -> UserGetSchema:
    print(token)
    db_user = get_current_user(token, db)
    return db_user


@router.post("/login", description="Authentifie un utilisateur et retourne un jwt token", response_model=jwtTokenSchema, status_code=200)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    db_user : User = db.query(User).filter(User.username == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise IncorrectCredentialsException()
    elif db_user.is_active == False:
        raise UnauthorizedException()
    elif db_user.password_expiration_delay != -1 and (db_user.date_updated + timedelta(days=db_user.password_expiration_delay)).replace(tzinfo=None) < datetime.now().replace(tzinfo=None):
        update_password_expired(db_user=db_user, db=db)
    expire_time = 30
    jwt_token = create_access_token(form_data.username, expire_time)
    jwt_refresh_token = create_refresh_token(form_data.username, expire_time + 20)
    db_Token = Token(user_id = db_user.id, access_token = jwt_token, refresh_token = jwt_refresh_token, expires_in = datetime.utcnow() + timedelta(minutes=expire_time))
    db.add(db_Token)
    db.commit()

    return {"token": {
        "access_token": db_Token.access_token,
        "refresh_token": db_Token.refresh_token,
        "expires_in": db_Token.expires_in
    },
            "password_expired": db_user.password_expired}


@router.post("/logout", description="Détruit le jwt Token de l'utilisateur et termine sa session", status_code=204)
async def logout(token: Annotated[str, Depends(jwtBearerScheme)], db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    if not current_user:
        raise CredentialsException() 
    db_token = db.query(Token).where(Token.access_token == token).one()
    db.delete(db_token)
    db.commit()


@router.post("/refresh-token", description="Rafraichis le token d'authentification", response_model=jwtTokenSchema, status_code=201)
async def refresh_user_token(token: str, db : Session = Depends(get_db)):
    db_token = db.query(Token).where(Token.refresh_token == token).first()
    current_user = db.query(User).where(User.id == db_token.user_id).one_or_none()
    if not current_user:
        raise CredentialsException
    if not db_token:
        raise CredentialsException()
    print("new db token")
    new_db_token = refresh_token(db_token)
    db.delete(db_token)
    db.commit()
    db.add(new_db_token)
    db.commit()
    db.refresh(new_db_token)
    return {"token": new_db_token,
            "password_expired": current_user.password_expired}


@router.put("/profile", description= "Met à jour le profil de l'utilisateur", status_code=202)
async def update_profile(token: Annotated[str, Depends(jwtBearerScheme)], updated_user: UpdateUserSchema, db : Session = Depends(get_db)):
    current_user: User = get_current_user(token, db)
    user_data = updated_user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(current_user, key, value)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return {"message": "user updated"}


@router.patch("/forgot-password", description="Créé et renvoie un lien pour réinitialiser le mot de passe oublié si l'utilisateur existe.", status_code=202)
async def forgot_password(user_login: str, base_url: str = None, db: Session = Depends(get_db)):
    db_user: User = None
    field: str = "email" if "@" in user_login else "username" # Dynamic Attribute getter
    db_user: User = db.query(User).filter(User.__getattribute__(User, field) == user_login).one_or_none()
    if db_user is None:
        return
    elif db_user.is_active == False:
        raise UnauthorizedException()
    reset_link = await create_reset_link(db_user=db_user, db=db)
    print(db_user.password_reset_link)
    return {"message": "Un lien de réinitialisation a été créer. SVP contacter votre administrateur pour qu'il vous envoie le lien de réinitialisation."}


@router.patch("/reset-password/{reset_password_link}", description="Change le mot de passe de l'utilisateur si le lien existe.", status_code=202)
async def reset_password(reset_password_link: str, updated_password: UpdateUserPasswordSchema, db: Session = Depends(get_db)):
    if reset_password_link is not None:
        db_user: User = db.query(User).filter(User.password_reset_link == reset_password_link).one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Le lien de réinitialisation n'existes pas ou est expiré.") #en: The reset password link has expired or does not exist.
    await update_password(db_user=db_user, updated_password=updated_password, db=db)
    return


@router.patch("/change-password", description="Met à jour le mot de passe de l'utilisateur.", status_code=202)
async def update_password(token: Annotated[str, Depends(jwtBearerScheme)], updated_password: UpdateUserPasswordSchema, db : Session = Depends(get_db)):
    current_user : User = get_current_user(token, db)
    await update_password(db_user=current_user, updated_password=updated_password, db=db)


async def update_password(db_user: User, updated_password: UpdateUserPasswordSchema, db: Session):
    """
    Update le mot de passe de l'utilisateur.

    Parameters
    ----------
    db_user: Utilisateur à changer le mot de passe.
    updated_password: Formulaire pour update le mot de passe.
    db: Instance de la connection à la db.
    """
    db_user.password_changed = True
    if updated_password.password_expiration_delay is None:
        db_user.password_expiration_delay = -1 # Might need to change to a specific delay
    else:
        db_user.password_expiration_delay = updated_password.password_expiration_delay
    db_user.password_expired = False
    db_user.hashed_password = get_hashed_password(updated_password.password)
    db_user.password_reset_link = None
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

