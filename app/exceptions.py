from fastapi import HTTPException, status

class IncorrectCredentialsException(HTTPException):
    def __init__(self):
        self.status_code=status.HTTP_401_UNAUTHORIZED
        # self.detail="Incorrect username or password" // english version.
        self.detail="Nom d'utilisateur ou mot de passe incorrect."

class UnauthorizedException(HTTPException):
    def __init__(self):
        self.status_code=status.HTTP_403_FORBIDDEN
        # self.detail="You are not authorized to view this content."
        self.detail="Vous n'êtes pas authorisé à accéder ce contenu."
        
class EntityNotFoundException(HTTPException):
    def __init__(self, name, field = None,  value = None):
        self.status_code=status.HTTP_400_BAD_REQUEST
        if id is not None:
            # self.detail=f"{name} with {field} [ {value} ] not found."
            self.detail=f"{name} Avec le champ {field} [ {value} ] a été trouvé."

        else:
            self.detail=f"Aucun(e) {name} trouvé(e)."

class CredentialsException(HTTPException):
    def __init__(self):
        self.status_code=status.HTTP_401_UNAUTHORIZED
        # self.detail="Could not validate credentials"
        self.detail="Impossible de valider les identifiants."

class DuplicateException(HTTPException):
    def __init__(self, field, value):
        self.status_code=status.HTTP_400_BAD_REQUEST
        # self.detail= f"User with {field} {value} already exists."
        self.detail= f"Utilisateur avec {field} {value} existe déjà."

class ValueErrorException(HTTPException):
    def __init__(self, message):
        self.status_code=status.HTTP_400_BAD_REQUEST
        self.detail = message

class FailedToCreateException(HTTPException):
    def __init__(self, entity_name):
        self.status_code = status.HTTP_400_BAD_REQUEST
        # self.detail = f"Failed to create {entity_name}."
        self.detail = f"La création d'un(e) {entity_name} à échoué(e)."