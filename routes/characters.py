# routers/characters.py
"""Character-related API endpoints."""

import json
import os
from fastapi import APIRouter, Body, Path, HTTPException, Request
from fastapi.responses import JSONResponse
from pathlib import Path as FilePath
from typing import Any, List

from pydantic import BaseModel, Field

from src.aiplayer import CHARACTER_DIRECTORY as CHARACTERS_DIR
from utils.file_operations import read_json_file, write_json_file

router = APIRouter(
    prefix="/characters",
    tags=["Characters"]
)

class CharacterModel(BaseModel):
    name: str = Field(..., description="Name of the character")
    persona: str = Field(..., description="Character persona description")
    examples: List[str] = Field(default_factory=list, description="Example interactions")
    instructions: str = Field("", description="Special instructions for the character")
    avatar: str = Field("", description="URL or path to avatar image")
    info: str = Field("", description="Additional info about the character")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Character1",
                "persona": "A helpful assistant",
                "examples": ["User: How are you? Character: I'm doing great!"],
                "instructions": "Always be polite and helpful",
                "avatar": "/images/char1.png",
                "info": "Created on May 6, 2025"
            }
        }


@router.get("/", response_model=List[str])
async def list_characters():
    """List all available characters."""
    try:
        if not os.path.exists(CHARACTERS_DIR):
            return []
        return [f.stem for f in FilePath(CHARACTERS_DIR).glob("*.json")]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/import_character")
async def importo_character(request: Request):
    """Import a character from raw JSON data."""
    try:
        body_bytes = await request.body()
        print("Raw request body (bytes):", body_bytes[:200]) # Print first 200 bytes

        try:
            # Explicitly decode from UTF-8 (most common for web)
            body_str = body_bytes.decode('utf-8')
            print("Decoded request body (string):", body_str[:200] + "...")
        except UnicodeDecodeError as ude:
            print(f"UnicodeDecodeError: {str(ude)}")
            raise HTTPException(status_code=400, detail=f"Invalid character encoding. Expected UTF-8. Error: {str(ude)}")

        try:
            character_data = json.loads(body_str)
            print("Parsed JSON data:", character_data)
        except json.JSONDecodeError as jde:
            print(f"JSON decode error: {str(jde)}")
            # You can include more context from jde if needed, e.g., jde.lineno, jde.colno
            raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(jde)}")

        print("About to convert data to CharacterModel")
        character = convert_to_character_model(character_data)
        print("Conversion successful:", character)
        if not character:
            raise HTTPException(status_code=500, detail=f"Import failed, Incompatible Card Format")
        
        # Use the existing create endpoint logic
        file_path = f"{CHARACTERS_DIR}/{character.name}.json"
        if os.path.exists(file_path):
            raise HTTPException(status_code=409, detail=f"Character '{character.name}' already exists")
        
        character_dict = character.dict()
        write_json_file(file_path, character_dict)
        return character_dict
    except Exception as e:
        print("Exception occurred:", str(e), type(e))
        # Return a 500 error with the exception details for debugging
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")

def convert_to_character_model(raw_data: dict) -> CharacterModel:
    print("Try Converting...")
    
    if raw_data.get("data",None) != None:
        try:
            print("Pygmalion Type Card")
            raw_data = raw_data.get("data",None)
            name= raw_data.get("name")
            description = raw_data.get("description","")
            examples = raw_data.get("mes_example","")
            personality = raw_data.get("personality","")
            system_prompt = raw_data.get("system_prompt","")
            post_history = raw_data.get("post_history_instructions","")
            avatar = raw_data.get("avatar","")
            if not name:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to convert data to CharacterModel, Json Format Not Supported (yet)"
                )
            description = description.replace("{{user}}","User")
            description = description.replace("{{char}}",name)
            examples = examples.replace("{{user}}","User")
            examples = examples.replace("{{char}}",name)           
            character = CharacterModel(
                name= name,
                persona=f"<description>{description}</description>\n<examples>{examples}</examples>\n<personality>{personality}</personality>\n",
                examples=[],
                instructions=f"[System Note: {system_prompt}]\n[System Note: {post_history}]",
                avatar=avatar
            )
            return character
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to convert data to CharacterModel: {str(e)}"
            )
    else:
        try:
            print("Viel Type Card")
            type = raw_data.get("type","")
            if type == "viel-card":
                print("Is Valid Viel Card")
                return CharacterModel(
                    name = raw_data.get("name"),
                    persona = raw_data.get("persona",""),
                    examples=raw_data.get("examples",[]),
                    instructions= raw_data.get("instructions",""),
                    avatar=raw_data.get("avatar","")
                )
        except Exception as e:
            print(e)
            raise HTTPException(
                    status_code=400,
                    detail=f"Failed to convert data to CharacterModel, Json Format Not Supported (yet)"
                )

@router.get("/{character_name}", response_model=CharacterModel)
async def get_character(character_name: str = Path(..., description="Name of the character")):
    """Get a character's configuration."""
    file_path = f"{CHARACTERS_DIR}/{character_name}.json"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Character '{character_name}' not found")
    
    data = read_json_file(file_path)
    return data

@router.post("/{character_name}", response_model=CharacterModel)
async def create_character(
    character_name: str = Path(..., description="Name of the character"),
    character: CharacterModel = Body(..., description="Character data")
):
    """Create a new character configuration."""
    file_path = f"{CHARACTERS_DIR}/{character_name}.json"
    if os.path.exists(file_path):
        raise HTTPException(status_code=409, detail=f"Character '{character_name}' already exists")
    
    character_dict = character.dict()
    write_json_file(file_path, character_dict)
    return character_dict

@router.put("/{character_name}", response_model=CharacterModel)
async def update_character(
    character_name: str = Path(..., description="Name of the character"),
    character: CharacterModel = Body(..., description="Updated character data")
):
    """Update an existing character configuration."""
    file_path = f"{CHARACTERS_DIR}/{character_name}.json"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Character '{character_name}' not found")
    
    character_dict = character.dict()
    write_json_file(file_path, character_dict)
    return character_dict

@router.delete("/{character_name}")
async def delete_character(character_name: str = Path(..., description="Name of the character")):
    """Delete a character configuration."""
    file_path = f"{CHARACTERS_DIR}/{character_name}.json"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Character '{character_name}' not found")
    
    try:
        os.remove(file_path)
        return JSONResponse(content={"message": f"Character '{character_name}' deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete character: {str(e)}")