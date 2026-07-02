from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.connection import get_db

from backend.schemas.auth_schema import SignupRequest, LoginRequest
from backend.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup")
def signup(user: SignupRequest, db: Session = Depends(get_db)):
    """
    Create a new user account.
    """
    return AuthService.signup(db, user)


@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    """
    Login an existing user.
    """
    return AuthService.login(db, user)