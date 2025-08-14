"""
Module for authentication route
"""
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api_service.schemas.user import User, UserResponse
from api_service.schemas.auth import Token
from api_service.core.mssql_session import get_mssql_connection
from api_service.services.auth import Authentication

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# If a user is new to the service - should add a route to allow them to register
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(
    user: User, 
    db: Session = Depends(get_mssql_connection)
    ): # Need to create the user schema before adding parameter
    """
    Create user account.
    """
    new_user = Authentication(db).create_new_user(user, response=True)
    return new_user

@router.post("/token", response_model=Token)
def login_user(
    user_form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_mssql_connection)
    ):
    """
    User authentication
    """
    return Authentication(db).authenticate(user_form)
