import os
from sqlalchemy.engine import URL
from pydantic_settings import BaseSettings

class DatabaseConfig:
    """
    SQL Server database configuration
    """
    def __init__(
            self, 
            driver:str, 
            server:str, 
            name:str, 
            username:str, 
            password:str
            ):
        """
        Initialize class instance for database connection

        params:
            - driver (str): database driver (odbc)
            - server (str): database server string (AWS RDS)
            - name (str): database name
            - username (str): SQL account username
            - password (str): SQL account password
        """
        self.driver = driver
        self.server = server
        self.database = name
        self.username = username
        self.password = password

    def create_dsn(self):
        connection_string = (
            f'DRIVER={self.driver};'
            f'SERVER={self.server};'
            f'DATABASE={self.database};'
            f'UID={self.username};'
            f'PWD={self.password};'
            'TrustServerCertificate=yes'
        )

        connection_dsn = URL.create("mssql+pyodbc", 
                            query={"odbc_connect": connection_string})
        
        return connection_dsn

class Settings(BaseSettings):
    # SQL env variables
    database_driver: str = os.getenv('SQL_driver')
    database_server: str = os.getenv('SQL_server')
    database_name: str = os.getenv('SQL_database')
    database_username: str = os.getenv('SQL_username')
    database_password: str = os.getenv('SQL_password')

    # Authentication env variables
    secret_key: str = os.getenv("JWT_SECRET_KEY") # Need to create a new secret key for this application
    algorithm: str = os.getenv("JWT_ALGORITHM")
    access_token_expire_minutes: int = os.getenv("JWT_EXPIRE_MINUTES")
    token_type: str = os.getenv("JWT_TOKEN_TYPE")

    # Kafka env variables 
    bootstrap_server: str = os.getenv("KAFKA_SERVERS")
    topic: str = os.getenv("KAFKA_TOPIC")

    mssql_dsn: DatabaseConfig = DatabaseConfig(
        driver=database_driver,
        server=database_server,
        name=database_name,
        username=database_username,
        password=database_password
    )

settings = Settings()
