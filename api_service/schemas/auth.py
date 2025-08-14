"""
Module for authentication schema
"""
from typing import Optional, Annotated
from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: Annotated[str, Field(description="Access token needed for service authentication")]
    token_type: Annotated[str, Field(description="Token Type")]

    model_config = {
    "json_schema_extra": {
        "examples": [
            {
                "access_token": '6e7e6a4a-d347-4232-a902-54fc57c6455f',
                "token_type": 'Bearer'
            }
        ]
    }
}

class TokenVal(BaseModel):
    id: Annotated[Optional[int], Field("User id for user account")] = None
