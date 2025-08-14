from datetime import datetime
from sqlmodel import Field, SQLModel, MetaData
from sqlalchemy import func

class Users(SQLModel, table=True):
    metadata = MetaData(schema="test")

    id: int | None = Field(default=None, primary_key=True, nullable=False)
    email: str = Field(max_length=255, nullable=False, unique=True)
    password: str = Field(max_length=255, nullable=False)
    last_updated: datetime = Field(sa_column_kwargs={"server_default": func.now()})
