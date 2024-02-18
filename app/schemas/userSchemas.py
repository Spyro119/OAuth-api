import re
from pydantic import BaseModel, FieldValidationInfo, model_validator, field_validator, Field
from datetime import datetime
from app.schemas.groupSchemas import GroupSchema
from app.exceptions import ValueErrorException

class UserSchema(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    password_changed: bool = False
    password_expiration_delay: int = 30
    password_expired: bool = True
    password_reset_link: str | None
    is_active: bool = False
    date_created: datetime
    date_updated: datetime | None
    groups: list[GroupSchema] | None

    class Config:
        from_attributes = True


class UpdateUserSchema(BaseModel):
    username: str
    first_name: str = None
    last_name: str = None
    email: str = None
    date_updated: datetime | None

    @field_validator("email")
    @classmethod
    def verify_email(cls, value: str) -> str:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(regex, value):
            # raise ValueErrorException("The email entered is not valid.")
            raise ValueErrorException("Le courriel entré n'est pas valide.")
        return value


class UserRegisterSchema(BaseModel):
    email: str
    first_name: str
    last_name: str
    username: str
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)
    password_changed: bool = False


    # @TODO faire en sorte que ça trigger avant la validation de champs.
    @model_validator(mode="after")
    def verify_password_match(self):
        password = self.password
        confirm_password = self.confirm_password

        if password != confirm_password:
            # raise ValueErrorException("The two passwords did not match.")
            raise ValueErrorException("Les mots de passes ne correspondent pas.")
        return self
    
    @field_validator("email")
    @classmethod
    def verify_email(cls, value: str) -> str:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(regex, value):
            # raise ValueErrorException("The email entered is not valid.")
            raise ValueErrorException("Le courriel entré n'est pas valide.")
        
        return value


    @field_validator("password", "confirm_password")
    @classmethod
    def verify_password(cls, value: str) -> str:
        regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        if not re.fullmatch(regex, value):
            # raise ValueErrorException(f'password must be at least 8 characters, include a special character, an uppercase character and a number.')
            raise ValueErrorException(f'Le mot de passe doit contenir au moins 8 charactères, inclure un charactère spécial, un nombre et une lettre.')
        return value


class UserLoginSchema(BaseModel):
    username: str
    hashed_password: str


class UpdateUserPasswordSchema(BaseModel):
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)
    password_expiration_delay: int = 30 # Doit changer le mot de passe au 30 jours.

    # @TODO change mode from after to before
    @model_validator(mode="after")
    def verify_password_match(self):
        password = self.password
        confirm_password = self.confirm_password

        if password != confirm_password:
            # raise ValueErrorException("The two passwords did not match.")
            raise ValueErrorException("Les mots de passes ne correspondent pas.")
        
        return self
    
    
    @field_validator("password", "confirm_password")
    @classmethod
    def verify_password(cls, value: str) -> str:
        regex = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        if not re.fullmatch(regex, value):
            # raise ValueErrorException(f'Password must be at least 8 characters, include a special character, one number and one letter.')
            raise ValueErrorException(f'Le mot de passe doit contenir au moins 8 charactères, inclure un charactère spécial, un nombre et une lettre.')
        
        return value


class UserGetSchema(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password_changed: bool = False
    password_expiration_delay: int = 30
    password_expired: bool = True
    is_active: bool


class AdminCreateUserSchema(UserRegisterSchema):
    group_ids: list[int] | None = None