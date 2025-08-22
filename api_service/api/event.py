"""
Module for event route
"""
from fastapi import APIRouter, Depends, status

from api_service.services.auth import get_current_user
from api_service.core.utils import get_producer
from api_service.schemas import (
    event,
    message
)

router = APIRouter(
    prefix='/event',
    tags=['Game Event']
)

# Need to create a default response model and a pydantic schema of what that post event looks like
@router.post("", status_code=status.HTTP_201_CREATED)
async def post_event(
    event: event.GameEvent, 
    user = Depends(get_current_user), 
    producer = Depends(get_producer)
    ):
    """
    Post sports event payload
    """ 
    await producer.produce_message(
        key=f'event-key-{event.play_id}', #use the event id from the payload
        value=event
    )

    return message.Message(message="Event has been queued.") 
