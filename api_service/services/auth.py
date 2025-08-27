from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlmodel import select

from api_service.core.config import settings
from api_service.models.user import Users
from api_service.schemas.auth import Token, TokenVal
from api_service.schemas.user import User, UserSchema
from api_service.services.base import SessionBase, DataManager

# Set the auth barer
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_current_user(token_str: str = Depends(oauth_scheme)):
    """
    Authenticate current user

    params:
        - token_str (str): access token provided in request headers / authentication
    """
    http_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not verify credentials",
                                          headers={"WWWW-Authenticate": "bearer"})
    
    return AuthUtils.verify_access_token(token=token_str, exception=http_exception)

# Create a class for the password
class AuthUtils:
    @staticmethod
    def get_password_hash(password:str):
        """
        Hash password provided in auth/token route

        params:
            - password (str): password provided in request body
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password:str, hashed_password:str):
        """
        Verify password signature

        params:
            - plain_password (str): password string - hashed in database
            - hashed_password (str): hashed password from database
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def verify_access_token(
            token: str, 
            **kwargs
        ):
        """
        Verify authentication (JWT) token. Using this method to ensure the token has not expired.
        """
        credential_err = kwargs.get('expection')
        try:
            # First decode the payload
            decoded = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)

            id: str = decoded.get("id") # get the id or username from jwt payload
            exp: datetime = decoded.get("exp")
            if not id:
                raise credential_err
            
            # check to ensure the expire time is still valid
            if datetime.fromtimestamp(exp) < datetime.utcnow() is True:
                raise credential_err
            
            # eventually add a pydantic model below
            token_data = TokenVal(id=id)

        except JWTError:
            raise credential_err
        
        return token_data
    
class Authentication(AuthUtils, SessionBase):
    """
    Auth class to create new users, create tokens, and authenticate
    a users token for API access
    """
    # authenticate and create jwt token
    def authenticate(
            self,
            login: OAuth2PasswordRequestForm = Depends()
    ):
        """
        Authenticate user credentials. This will check the email and password match what is in
        the application database (company internal records)
        """
        # Return user information bassed on the email
        user_info = AuthDataService(self.session).get_user(login.username)

        if not login.password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid credentials")
        
        if self.verify_password(login.password, user_info.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid credentials")

        access_token = self._create_access_token(user_info.id, user_info.email)
        return Token(access_token=access_token, token_type=settings.token_type)
        
    # Create new user method
    def create_new_user(
            self, 
            user: User,
            response:bool = False
        ):
        """
        Add new user credentials to database

        params:
            - user (dict): user dictionary posted to API route
            - response (bool): flag to determine if user info is returned
        """
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid request")
        
        user_res = Users(
            email=user.email,
            password=self.get_password_hash(user.password)
        )

        res_return = AuthDataService(self.session).add_user(user_res, response=response)
        return res_return

    def _create_access_token(
            self, 
            id: int, 
            email: EmailStr
        ):
        """
        Creating access token

        params:
            - id (int): user id from internal database
            - email (str): user email used to register account
        """
        to_encode = {
            "id": id,
            "sub": email,
            "exp": self._set_expire_time()
        }

        return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    # set expire time internal method
    @staticmethod
    def _set_expire_time():
        """
        Set JWT token expire time. The token will only be active
        for a set period of time determined by application developers
        """
        return datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

class AuthDataService(DataManager):
    """
    Class to handle database operations related to
    the user
    """
    def add_user(self, user: User, response:bool = True):
        res_dict = self.add_one(user, response=response)

        if res_dict is True:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="User account already exists. Please use different email or login")
        
        return res_dict
    
    def get_user(self, username: EmailStr) -> UserSchema:
        sql_model = self.get_one(
            select(Users).where(Users.email == username)
        )
        
        if not sql_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid credentials"
            )
        
        return UserSchema(
            id=sql_model.id,
            email=sql_model.email,
            password = sql_model.password,
            last_updated=sql_model.last_updated
        )
