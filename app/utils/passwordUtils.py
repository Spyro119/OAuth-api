import base64
import hashlib
import bcrypt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.utils.jwtHandler import create_refresh_token

from app.models.User import User

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    """
    hash le mot de passe et le renvoie.

    Parameters
    ----------
    password: mot de passe entré par l'utilisateur.
    """
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    """
    vérifie si le mot de passe concorde avec le mot de passe dans la db.

    Parameters
    ----------
    password: mot de passe entré par l'utilisateur
    hashed_pass: mot de passe de l'utilisateur sauvegardé dans la db.
    """
    return password_context.verify(password, hashed_pass)


async def create_reset_link(db_user: User, db: Session):
    """
    Créer un lien pour réinitialiser le mot de passe.

    Parameters
    ----------
    db_user: Utilisateur à changer le mot de passe.
    db: Instance de la connection à la db.
    """
    db_user.password_reset_link = create_refresh_token(db_user.email, 60)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user.password_reset_link


def update_password_expired(db_user: User, db: Session ):
    db_user.password_expired = True
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user