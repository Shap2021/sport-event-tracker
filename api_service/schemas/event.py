"""
Module for event schema.
"""
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Annotated

class GameEvent(BaseModel):
    game_id:int = Field(title="Game Identifier", description="Game Id for current game")
    play_id:Optional[str] = Field(description="Play Id of current game event")
    event_type:str = Field(description="Game event type (e.g. scoring, game started, pause in action, etc.)")
    event: str = Field(description="Game event (e.g. touchdown, field goal, tackle, etc.)")
    timestamp: Optional[datetime] = Field(default=None, description="Timestamp of current game event")
    player_id: int = Field(description="Player Id of player involved in current game event")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "game_id": 1,
                    "play_id": str(uuid4()),
                    "event_type": "scoring",
                    "event": "Touchdown!",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "player_id": 1234567
                }
            ]
        }
    }
    
    class Config:
        from_attributes = True
