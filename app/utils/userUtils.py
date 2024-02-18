from sqlalchemy.orm import Session

from app.schemas.userSchemas import UserSchema
from app.exceptions import UnauthorizedException, DuplicateException
from app.models.User import User
from app.models.jwtToken import Token as jwtToken
from app.schemas.userSchemas import UserRegisterSchema
from app.utils.jwtHandler import decode_token
from app.utils.passwordUtils import get_hashed_password


def get_current_user(token: jwtToken, db : Session) -> UserSchema | UnauthorizedException:
    """
    Retrouve les informations de l'utilisateurs connectés dans la db via son token.

    Parameters
    ----------
    token : Token d'authentification.
    db : Instance permettant la connection à la db.
    """
    username : str = decode_token(token)
    if username is None:
        raise UnauthorizedException()
    current_user: UserSchema = db.query(User).filter(User.username == username).first()
    if current_user is None:
        raise UnauthorizedException()
    return current_user


def specify_duplicate_field(db_user: User, new_user: User) -> DuplicateException:
    """
    Spécifie quel champs est "dupliqué" dans la db.

    Parameters
    ----------
    db_user: Utilisateur trouvé dans la base de donnée.
    new_user: Nouvel utilisateur.
    db: Instance de la connection à la database.
    """
    if db_user.username == new_user.username:
            field = "username"
            value = new_user.username
    elif db_user.email == new_user.email:
        field = "email"
        value = new_user.email
    raise DuplicateException(field, value)


async def create_user(new_user: UserRegisterSchema, db: Session) -> User:
    """
    Créer un nouvel utilisateur.
    
    Parameters
    ----------
    new_user: Nouvel utilisateur.
    db: Instance de la connection à la database.
    """
    db_user = db.query(User).filter(User.username == new_user.username or User.email == new_user.email).one_or_none()
    if db_user is not None:
        specify_duplicate_field(db_user, new_user)

    password = get_hashed_password(new_user.password)
    db_user = User(email = new_user.email, 
                   username = new_user.username, 
                   first_name= new_user.first_name, 
                   last_name= new_user.last_name, 
                   hashed_password = password,
                   password_changed = new_user.password_changed if new_user.password_changed is not None else False,
                   password_expired = False if new_user.password_changed else True # Requires user to change his password on first login
                   )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user