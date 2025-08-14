"""
Module for base instances of util classes
"""
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

class SessionBase:
    """
    Initializing database session
    """
    def __init__(self, session: Session):
        self.session = session

# A class that does select one, add a row, etc
class DataManager(SessionBase):
    """
    Class responsible for database operations
    """
    def add_one(self, model, response:bool = False):
        try:
            self.session.add(model)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            return True
        
        if response is True:
            self.session.refresh(model)
            return model

    def get_one(self, sql_stmt):
        return self.session.exec(sql_stmt).first()
