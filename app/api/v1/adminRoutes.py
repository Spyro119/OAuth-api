from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session

from app.schemas.userSchemas import UserSchema, UserRegisterSchema, AdminCreateUserSchema
from app.schemas.PermissionSchemas import PermissionSchema
from app.schemas.groupSchemas import GroupSchema, AdminCreateGroupSchema
from app.models.Permission import Permission
from app.models.PermissionGroup import Permission_group
from app.models.User import User
from app.models.Group import Group
from app.models.UserGroup import User_Group

from app.utils.userUtils import create_user
from app.db.session import get_db
from app.exceptions import EntityNotFoundException
from app.utils.jwtHandler import JWTBearer

allow_create_resource = JWTBearer(allowed_roles=["Admin"]) 

admin_router = APIRouter(
                prefix='/api/v1/admin',
                tags = ['/api/v1/admin'],
                dependencies=[Depends(allow_create_resource)],
            )


@admin_router.get("/Permissions", description="Retourne toutes les permissions",response_model=list[PermissionSchema] )
async def get_permissions(db : Session = Depends(get_db)):
    db_permissions = db.query(Permission).all()
    if db_permissions is None:
        raise EntityNotFoundException("Permissions")
    return db_permissions


@admin_router.get("/groups", description="Liste les groupes.", response_model=list[GroupSchema])
async def get_groups(db : Session = Depends(get_db)):
    db_groups = db.query(Group).all()
    if db_groups is None:
        raise EntityNotFoundException("Groups")
    return db_groups


@admin_router.get("/groups/{id}", description="Retourne un groupe.", response_model=GroupSchema)
async def get_group(id: int, db : Session = Depends(get_db)):
    db_group = db.query(Group).get(id)
    if db_group is None:
        raise EntityNotFoundException("Groups","id", id)
    return db_group


@admin_router.get("/users", description="Liste les utilisateurs", response_model=list[UserSchema])
def get_users(db: Session = Depends(get_db)):
    db_users = db.query(User).all()
    if db_users is None:
        raise EntityNotFoundException("Users")
    return db_users


@admin_router.get("/user/{id}", description="Retourne un utilisateur.", response_model=UserSchema)
async def get_user(id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).get(id)
    if db_user is None:
        raise EntityNotFoundException("User", "id", id)
    return db_user


@admin_router.post("/group", description="Créé un nouveau groupe, (Optionnel) assigne des utilisateurs et permissions au nouveau groupe.", status_code=status.HTTP_201_CREATED, response_model=GroupSchema)
async def create_group(new_group: AdminCreateGroupSchema, db : Session = Depends(get_db)):
    db_group = Group(name = new_group.name,
                    description = new_group.description,
                    is_active = new_group.is_active)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    print(new_group.user_ids)
    if new_group.user_ids is not None:
        print(len(new_group.user_ids))
        await bulk_add_users_to_group(new_group.user_ids, db_group, db)
    if new_group.permission_ids is not None:
        await bulk_add_permissions_to_group(new_group.permission_ids, db_group, db)
    return db_group


@admin_router.post("/create-admin", description="Créé un nouvel administrateur.", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_admin(new_user: UserRegisterSchema, base_url: str = None, db : Session = Depends(get_db)):
    # new_user.password_changed = True
    db_user = await create_user(new_user, db)
    db_group = db.query(Group).where(Group.name == "Admin").one()
    await bulk_add_groups_to_user(group_ids=[db_group.id], db_user=db_user, db=db)
    db.refresh(db_user)
    return db_user


@admin_router.post("/create-user",description="Créé un nouvel utilisateur, (Optionnel) assigne l'utilisateur à des groupes.", response_model=UserSchema, status_code=status.HTTP_200_OK)
async def insert_user(new_user: AdminCreateUserSchema, base_url: str = None, db : Session = Depends(get_db)):
    db_user = await create_user(new_user, db)
    if new_user.group_ids is not None:
        await bulk_add_groups_to_user(group_ids=[new_user.group_ids], db_user=db_user, db=db)
    return db_user


@admin_router.post("/add-groups-to-user", description="Assigne un/des groupe(s) à un utilisateur.", status_code=status.HTTP_202_ACCEPTED)
async def add_groups_to_user(user_id: int, group_ids: list[int], db : Session = Depends(get_db)):
    db_user : User = db.query(User).get(user_id)
    if db_user is None:
        raise EntityNotFoundException("User", "id", db_user.id)
    message: str = await bulk_add_groups_to_user(group_ids, db_user, db)
    return {"message": message}


@admin_router.post("/add-permissions-to-group", description="Assigne un/des groupe(s) à un utilisateur.", status_code=status.HTTP_202_ACCEPTED)
async def add_permissions_to_group(group_id: int, permission_ids: list[int], db : Session = Depends(get_db)):
    db_group : Group = db.query(Group).get(group_id)
    if db_group is None:
        raise EntityNotFoundException("Group", "id", group_id)
    message: str = await bulk_add_permissions_to_group(permission_ids, db_group, db)
    return {"message": message}


@admin_router.post("/add-users-to-group", description="Assigne un/des utilisateur(s) à un groupe.", status_code=status.HTTP_202_ACCEPTED)
async def add_users_to_group(group_id: int,user_ids: list[int],db : Session = Depends(get_db)):
    db_group: Group = db.query(Group).get(group_id)
    if db_group is None:
        raise EntityNotFoundException("Group", "id", db_group.id)
    message: str = await bulk_add_users_to_group(user_ids, db_group, db)
    return {"message": message}

# @TODO verify
@admin_router.delete("/remove-permissions-from-group", description="Supprimes une/des permission(s) d'un groupe.", status_code=status.HTTP_202_ACCEPTED)
async def remove_permissions_from_group(permission_ids: list[int], group_id: int, db: Session = Depends(get_db)):
    permission_codes = []
    db_group = db.query(Group).get(group_id)
    if db_group is None:
        raise EntityNotFoundException("Group", "id", group_id)
    db_permission_group = db.query(Permission_group).where(Permission_group.group_id == group_id and Permission_group.permission_id.in_(permission_ids)).all()
    for permission_group in db_permission_group:
        db_permission = db.query(Permission).get(permission_group.permission_id)
        permission_codes.append(db_permission.code)
    if not db_permission_group:
        raise EntityNotFoundException("Permission group")
    db_delete = Permission_group.__table__.delete().where(Permission_group.group_id == group_id and Permission_group.permission_id.in_(permission_ids))
    db.execute(db_delete)
    db.commit()
    return {"message": f"Permission(s) [ {permission_codes} ] supprimée(s) du groupe {db_group.name} avec succès"}


@admin_router.delete("/remove-groups-from-users", description="Supprimes un/des utilisateur(s) d'un groupe.", status_code=status.HTTP_202_ACCEPTED)
async def remove_groups_from_users(group_ids: list[int], user_id: int, db: Session = Depends(get_db)):
    group_names = []
    db_user : User = db.query(User).get(user_id)
    if db_user is None:
        raise EntityNotFoundException("User", "id", user_id)
    db_user_groups: list[User_Group] = db.query(User_Group).where(User_Group.user_id == user_id and User_Group.group_id.in_(group_ids)).all()
    for user_group in db_user_groups:
        db_group: Group = db.query(Group).get(user_group.group_id)
        group_names.append(db_group.name)
    if not db_user_groups:
        raise EntityNotFoundException("User groups")
    db_delete = User_Group.__table__.delete().where(User_Group.user_id == user_id and User_Group.group_id.in_(group_ids))
    db.execute(db_delete)
    db.commit()
    return {"message": f"Groupe(s) [ {group_names} ] retiré(s) de l'utilisateur {db_user.username} avec succès."}


@admin_router.delete("/remove-users-from-group", description="Supprime un/des groupe(s) d'un utilisateur.", status_code=status.HTTP_202_ACCEPTED)
async def remove_users_from_group(user_ids: list[int], group_id, db: Session = Depends(get_db)):
    user_names = []
    db_group : Group = db.query(Group).get(group_id)
    if db_group is None:
        raise EntityNotFoundException("Group", "id", group_id)
    db_user_groups: list[User_Group] = db.query(User_Group).where(User_Group.group_id == group_id and User_Group.user_id.in_(user_ids)).all()
    for user_group in db_user_groups:
        db_user: User = db.query(User).get(user_group.user_id)
        user_names.append(db_user.username)
    if not db_user_groups:
        raise EntityNotFoundException("User groups")
    db_delete = User_Group.__table__.delete().where(User_Group.group_id == group_id and User_Group.user_id.in_(user_ids))
    db.execute(db_delete)
    db.commit()
    return {"message": f"Utilisateur(s) {user_names} supprimé(s) du groupe {db_group.name} avec succès"}


@admin_router.delete("/delete-groups", description="Supprime un/des groupe(s)", status_code=status.HTTP_202_ACCEPTED)
async def bulk_delete_groups(group_ids: list[int], db: Session = Depends(get_db)):
    db_groups = db.query(Group).filter(Group.id.in_(group_ids)).all()
    if db_groups is None or db_groups == []:
        raise EntityNotFoundException("Groups", "ids", group_ids)
    db_delete_user_group = User_Group.__table__.delete().where(User_Group.group_id.in_(group_ids))
    print(db_delete_user_group)
    db.execute(db_delete_user_group)
    db.commit()

    db_delete_group_permission = Permission_group.__table__.delete().where(Permission_group.group_id.in_(group_ids))
    db.execute(db_delete_group_permission)
    db.commit()

    db_groups = Group.__table__.delete().filter(Group.id.in_(group_ids))  # db.query(Group).filter(Group.id in group_ids).all()

    db.execute(db_groups)
    db.commit()
    return {"message": "Groupe(s) supprimé(s) avec succès!"}


@admin_router.delete("/delete-users", description="Supprime un/des utilisateur(s)", status_code=status.HTTP_202_ACCEPTED)
async def bulk_delete_users(user_ids: list[int], db: Session = Depends(get_db)):
    db_users = db.query(User).where(User.id.in_(user_ids)).all()
    if db_users is None:
        raise EntityNotFoundException("Users", "ids", user_ids)
    db_delete_user_groups = User_Group.__table__.delete().where(User_Group.user_id.in_(user_ids))
    db.execute(db_delete_user_groups)
    db.commit()

    db_delete_users = User.__table__.delete().where(User.id.in_(user_ids))
    db.execute(db_delete_users)
    return {"message": "Utilisateur(s) supprimé(s) avec succès!"}
        

async def bulk_add_users_to_group(user_ids: list[int], db_group: Group, db: Session ) -> str | EntityNotFoundException:
    """
    Ajoute un/des utilisateur(s) à un groupe.

    Parameters
    ----------
    user_ids: liste d'IDs d'utilisateur à ajouter au groupe.
    group: Groupe à update.
    db: Instance de la connection à la database.
    """
    db_user_groups: list[User_Group] = []
    db_users: list[User] = db.query(User).filter(User.id.in_(user_ids)).all()
    if db_users is None or db_users == []:
        raise EntityNotFoundException("User")
    user_names: list[str] = [user.username for user in db_users]
    for user in db_users:
        db_user_groups.append(User_Group(user_id=user.id, group_id=db_group.id))
    db.bulk_save_objects(db_user_groups)
    db.commit()
    db.refresh(db_group)
    return f"Ajout du groupe {db_group.name} à/aux utilisateur(s) {user_names} avec succès!"


async def bulk_add_permissions_to_group(permission_ids: list[int], db_group: Group, db: Session) -> str | EntityNotFoundException:
    """
    Ajoute une/des permission(s) à un groupe.

    Parameters
    ----------
    permission_ids: liste d'IDs de permissions à ajouter au groupe.
    group_id: ID du groupe à update.
    db: Instance de la connection à la database.
    """
    db_permission_groups: list[Permission_group] = []
    db_permissions : Permission = db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
    if db_permissions is None:
        raise EntityNotFoundException("Permissions", "id", permission_ids)
    
    permission_codes : list[str] = [permission.code for permission in db_permissions]
    for permission_id in permission_ids:
        db_permission_groups.append(Permission_group(group_id=db_group.id, permission_id=permission_id))
    
    db.bulk_save_objects(db_permission_groups)
    db.commit()
    return {"message": f"Ajout de la/des permission(s) {permission_codes} au groupe {db_group.name} avec succès!"}


async def bulk_add_groups_to_user(group_ids: list[int], db_user: User, db: Session) -> str | EntityNotFoundException:
    """
    Ajoute un/des groupe(s) à un utilisateur.

    Parameters
    ----------
    group_ids: liste d'IDs d'utilisateur à ajouter au groupe.
    group_id: ID du groupe à update.
    db: Instance de la connection à la database.
    """
    db_user_groups: list[User_Group] = []
    db_group : Group = db.query(Group).filter(Group.id.in_(group_ids)).all()
    if db_group is None:
        raise EntityNotFoundException("Group")
    
    group_names : list[str] = [group.name for group in db_group]
    for group_id in group_ids:
        db_user_groups.append(User_Group(user_id=db_user.id, group_id=group_id))
    
    db.bulk_save_objects(db_user_groups)
    db.commit()
    return f"Ajout du/des groupe(s) {group_names} à l'utilisateur {db_user.username} avec succès!"
