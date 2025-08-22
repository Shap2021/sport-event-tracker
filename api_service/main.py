"""
Application server file (main.py)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api_service.api import auth
from api_service.api import event
from api_service.services.producer import ProducerService

# Define lifespan to start the service for Kafka Message Queue
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    On application startup/stop: open or close Kakfa connection
    """
    app.state.producer = ProducerService()
    await app.state.producer.start()
    try:
        yield
    except Exception as err:
        print('Issue with Kafka producer service: ', err)
    finally:
        await app.state.producer.stop()
        del app.state.producer

app = FastAPI(title="Sports Event Microservice",
              lifespan=lifespan)

## Add middleware and CORS (Cross Origin Resource Sharing) below - when applicable
app.add_middleware(
    CORSMiddleware,
    allow_origins=[], # likely to be just localhost for local development and testing
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Authorization"]
)

app.include_router(auth.router)
app.include_router(event.router)

# Define a root or index route
@app.get("/", include_in_schema=False)
def root():
    """
    Root or index route for when the application is idle
    """
    return {"message": "Hello World!"}

@app.get("/health", include_in_schema=False)
def health_check():
    """
    Application health check route
    """
    return {"status": "ok"}
