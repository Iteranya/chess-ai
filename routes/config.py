# routers/config.py
"""Bot configuration API endpoints."""

import os
from fastapi import APIRouter, Body, HTTPException
from typing import List, Set
import json
from src.config import CONFIG_PATH as CONFIG_FILE
from pydantic import Field, BaseModel
from utils.file_operations import read_json_file, write_json_file


PRESERVE_FIELDS: Set[str] = {'ai_key', 'discord_key'}

REQUIRED_FIELDS: Set[str] = {'default_character', 'ai_endpoint', 'base_llm'}

router = APIRouter(
    prefix="/config",
    tags=["Bot Configuration"]
)

class BotConfigModel(BaseModel):
    default_character: str = Field("Viel", description="Default character name")
    ai_endpoint: str = Field("https://generativelanguage.googleapis.com/v1beta/openai/", 
                           description="AI API endpoint")
    base_llm: str = Field("gemini-2.5-pro-exp-03-25", description="Base LLM model name")
    temperature: float = Field(0.5, description="Temperature setting for AI generation")
    ai_key: str = Field("", description="AI API key")
    
    class Config:
        schema_extra = {
            "example": {
                "default_character": "Viel",
                "ai_endpoint": "https://generativelanguage.googleapis.com/v1beta/openai/",
                "base_llm": "gemini-2.5-pro-exp-03-25",
                "temperature": 0.7,
                "ai_key": "your-api-key",
            }
        }

@router.get("/", response_model=BotConfigModel)
async def get_config():
    """Get the bot configuration."""
    if not os.path.exists(CONFIG_FILE):
        # Return default config if file doesn't exist yet
        return BotConfigModel()
    
    data = read_json_file(CONFIG_FILE)
    return data

@router.put("/", response_model=BotConfigModel)
async def update_config(config: BotConfigModel = Body(..., description="Updated bot configuration")):
    """Update the bot configuration with smart field preservation."""
    try:
        # Load existing config if file exists
        existing_config = {}
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                existing_config = json.load(f)
        
        # Convert new config to dict
        new_config = config.dict()
        
        # Validate required fields aren't being set to empty
        for field in REQUIRED_FIELDS:
            if new_config.get(field, '').strip() == '':
                raise HTTPException(
                    status_code=400,
                    detail=f"Field '{field}' cannot be empty"
                )
        
        # Preserve existing values for specified fields if new value is empty
        for field in PRESERVE_FIELDS:
            if (field in existing_config and 
                field in new_config and 
                str(new_config[field]).strip() == ''):
                new_config[field] = existing_config[field]
        
        # Write the merged config
        write_json_file(CONFIG_FILE, new_config)
        return new_config
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating config: {str(e)}")