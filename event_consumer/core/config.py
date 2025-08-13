import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # mongodb env variables
    mongodb_username:str = os.getenv("MONGODB_USERNAME")
    mongodb_password:str = os.getenv("MONGODB_PASSWORD")
    mongodb_cluster:str = os.getenv("MONGODB_CLUSTER")
    mongodb_database:str = os.getenv("MONGODB_DATABASE")
    mongodb_collection:str = os.getenv("MONGODB_COLLECTION")

    # kafka env variables
    boostrap_server:str = os.getenv("KAFKA_SERVERS")
    topic:str = os.getenv("KAFKA_TOPIC")
    group_id:str = os.getenv("KAFKA_GROUP_ID")
    offset:str = os.getenv("KAFKA_OFFSET")



settings = Settings()
