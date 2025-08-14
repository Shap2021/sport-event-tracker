"""
Module for event schema.
"""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Annotated

class GameEvent(BaseModel):
    game_id:str = Field(title="Game Identifier", description="Game Id for current game")
    play_id:Optional[str] = Field(description="Play Id of current game event")
    event_type: str = Field(description="Game event type (e.g. touchdown, field goal, tackle, etc.)")
    timestamp: Optional[datetime] = Field(default=None, description="Timestamp of current game event")
    player_id: int = Field(description="Player Id of player involved in current game event")

    class Config:
        from_attributes = True
