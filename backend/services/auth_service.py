from sqlalchemy.orm import Session

from backend.models.auth_user import AuthUser
from backend.schemas.auth_schema import SignupRequest, LoginRequest

from backend.core.security import hash_password, verify_password
from backend.core.jwt_handler import create_access_token

class AuthService:

    @staticmethod
    def signup(db: Session, user: SignupRequest):

        # Check email
        existing_email = (
            db.query(AuthUser)
            .filter(AuthUser.email == user.email)
            .first()
        )

        if existing_email:
            return {
                "success": False,
                "message": "Email already exists."
            }

        # Check username
        existing_username = (
            db.query(AuthUser)
            .filter(AuthUser.username == user.username)
            .first()
        )

        if existing_username:
            return {
                "success": False,
                "message": "Username already exists."
            }

        new_user = AuthUser(
            username=user.username,
            email=user.email,
            password_hash=hash_password(user.password)
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "success": True,
            "message": "Account created successfully."
        }

    @staticmethod
    def login(db: Session, user: LoginRequest):

        db_user = (
            db.query(AuthUser)
            .filter(AuthUser.email == user.email)
            .first()
        )

        if not db_user:
            return {
                "success": False,
                "message": "Invalid email or password."
            }

        if not verify_password(
            user.password,
            db_user.password_hash
        ):
            return {
                "success": False,
                "message": "Invalid email or password."
            }

        token = create_access_token(
            {
                "user_id": db_user.id,
                "email": db_user.email
            }
        )

        return {
            "success": True,
            "access_token": token,
            "username": db_user.username,
            "email": db_user.email
        }