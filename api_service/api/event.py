"""
Module for event route
"""
from fastapi import APIRouter, Depends, status

from api_service.services.auth import get_current_user
from api_service.services.producer import producer
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
def post_event(event: event.GameEvent, user = Depends(get_current_user)):
    """
    Post sports event payload
    """ 
    producer.produce_message(
        key=f'event-key-{event.play_id}', #use the event id from the payload
        value=event
    )

    return message.Message(message="Event has been queued.")
