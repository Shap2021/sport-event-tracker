"""
Module for API response schema.
"""
from pydantic import BaseModel

class Message(BaseModel):
    message:str
