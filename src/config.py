import os,json
from dataclasses import dataclass,asdict
CONFIG_PATH =  "ai_config.json"

@dataclass
class Config:
    default_character: str = "Viel"
    ai_endpoint: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    base_llm: str = "gemini-2.5-pro-exp-03-25"
    temperature: float = 0.5
    ai_key: str = ""

def load_or_create_config(path: str = CONFIG_PATH) -> Config:
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
            current_config = Config(**data)
            current_config.ai_key = "" 
            return current_config
    else:
        default_config = Config()
        save_config(default_config, path)
        print(f"No config found. Created default at {path}.")
        default_config.ai_key = ""
        return default_config
    
def save_config(config: Config, path: str = CONFIG_PATH) -> None:
    with open(path, 'w') as f:
        json.dump(asdict(config), f, indent=2)

def get_key(path:str = CONFIG_PATH) -> str:
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
            current_config = Config(**data)
            return current_config.ai_key 
    else:
        return ""