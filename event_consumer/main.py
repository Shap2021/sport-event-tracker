"""
FastAPI App to consume Kafka messages to load to MongDB
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager

from services.consume_message import ConsumeMessage

# Define a lifespan to start and stop a service on app startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    await ConsumeMessage().start_service()
    try:
        yield
    except KeyboardInterrupt:
        print('Shutting down service...')
    finally:
        await ConsumeMessage().stop_service()

app = FastAPI(lifespan=lifespan)

# Define root path - 200 health checks
@app.get("/")
def root():
    return {"message": "Event consumer is running..."}
