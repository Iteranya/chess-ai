from openai import OpenAI
from src.config import load_or_create_config,Config,get_key
import re
import traceback
from src.aiplayer import AICharacter

def clean_string(s):
    # Matches only if the string starts with a single word (no spaces), followed by ':'
    return re.sub(r'^[^\s:]+:\s*', '', s) if re.match(r'^[^\s:]+:\s*', s) else s

def clean_thonk(s):
    # Find </think> and remove everything before it (including </think>)
    match = re.search(r'</think>', s)
    if match:
        # Recursively clean the remaining string
        return clean_thonk(s[match.end():])
    else:
        return s

async def generate_blank(system,user,assistant):
    try:
        ai_config: Config = load_or_create_config()

        client = OpenAI(
            base_url=ai_config.ai_endpoint,
            api_key=get_key(),
        )

        completion = client.chat.completions.create(
            model=ai_config.base_llm,
            temperature=ai_config.temperature,
            messages=[
                {
                    "role": "system",
                    "content": system
                },
                {
                    "role": "user",
                    "content":user
                },
                {
                    "role": "assistant",
                    "content": assistant
                }
            ]
        )

        result = completion.choices[0].message.content if completion.choices else f"//[Error]"
        result = clean_thonk(result)
    except Exception as e:
        result = str(e)
    return result

async def generate_in_character(system,user,assistant, character=None):
    ai_config: Config = load_or_create_config()

    if not character:
        character = ai_config.default_character

    bot = AICharacter(character)
    char_prompt = await bot.get_character_prompt()
    system_prompt = char_prompt + system

    try:

        client = OpenAI(
            base_url=ai_config.ai_endpoint,
            api_key=get_key(),
        )

        completion = client.chat.completions.create(
            model=ai_config.base_llm,
            temperature=ai_config.temperature,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content":user
                },
                {
                    "role": "assistant",
                    "content": assistant
                }
            ]
        )

        result = completion.choices[0].message.content if completion.choices else f"//[Error]"
        result = clean_thonk(result)
    except Exception as e:
        result = str(e)
    return result