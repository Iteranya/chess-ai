


from src.aiplayer import AICharacter
from src.chess import ChessGame


class PromptEngineer:
    def __init__(self,bot:AICharacter,chess:ChessGame):
        self.bot = bot # The Address... right???
        self.chess = chess # THE ADDRESS RIGHT???

    def prompt_after_player_turn(self): # Before AI turn
        personality = self.bot.get_character_prompt()
        history = self.chess.print_board()

        



# class PromptEngineer:
#     def __init__(self, bot:AICharacter, message: discord.Message, dimension:Dimension):
#         self.bot = bot
#         self.user = str(message.author.display_name)
#         self.message = message
#         self.dimension = dimension
#         self.stopping_string = None
#         self.prefill = None 
#         print(self.user)

#     async def create_text_prompt(self) -> str:
#         jb = self.bot.instructions
#         character = await self.bot.get_character_prompt()
#         #jb = "" # Toggle this to disable JB
#         globalvar = self.dimension.getDict().get("globalvar", "")
#         locationvar = self.dimension.getDict().get("location", "")
#         instructionvar = self.dimension.getDict().get("instruction", "")

#         if self.message.content.startswith("search>"):
#             try:
#                 search_query = self.message.content.replace("search>","")
#                 search_query = search_query.lower()
#                 search_query = search_query.replace(self.bot.bot_name.lower(),"") # Wait, why is it not working???
#                 print(search_query)
#                 search_result = await research(search_query)
#                 #print(search_result)
#                 instructionvar += search_result
#                 #print(instructionvar)
#             except Exception as e:
#                 print (e)

#         if "<battle_rp>" in self.dimension.instruction:
#             try:
#                 try:
#                     globalvar+= get_opponent(self.bot.bot_name,self.message)
#                 except Exception as e:
#                     pass
#                 instructionvar += roll_defend(self.bot.bot_name)
#                 instructionvar += roll_attack(self.bot.bot_name)
#             except Exception as e:
#                 print(e)
        
#         if"<tarot>" in self.message.content.lower():
#             tarot = generate_tarot_reading(self.message.content)
#             instructionvar+=f"[System Note: The following is the Tarot Shuffle Result, please have {self.bot.bot_name} interpret it in character. \n\n{tarot}]"

#         # Safety Filter for Discord ToS Sake, please don't disable. Just use NSFW Channel like a normal person.
#         try:
#             if not self.message.channel.is_nsfw():
#                 instructionvar+="\n\n[System Note: IMPORTANT, Strict Safety Filter Deployed. Bot MUST Refuse To Answer If Content Is Harmful, Sexual, or Controversial in Nature. Try To Stay In Character, But Prioritize Safety Above All Else.]"
#         except Exception as e:
#             print("In DM, all good")
#         history = await get_history(self.message)
#         print("Instruction ====== " + instructionvar)
#         prompt = (
#             f"<character_definition>{character}</character_definition>\n"
#             f"<lore>{globalvar}</lore>\n"
#             f"<conversation_history>{history}</conversation_history>\n"
#             f"<note>{locationvar}</note>\n"
#             f"<additional_note>{jb}\n{instructionvar}</additional_note>\n"
#         )
#         # JUST USE AN F STRING YOU GODDAMN NEANDERTHAL!!!!!
#         # SHUT THE FUCK UP I'M PROTOTYPING!!!
#         # THERE I USED FSTRING, HAPPY NOW?!!?!?
#         self.prefill = f"\n[Reply] {self.bot.name}:"
#         self.stopping_string = ["[System", "(System", self.user + ":", "[End","[/"] 
#         #print(prompt)
#         return prompt
    
#     async def create_smart_prompt(self)->str:
#         character = await self.bot.get_character_prompt()
#         tools = extract_plugin_docs_as_string()
#         globalvar = self.dimension.getDict().get("globalvar", "")
#         locationvar = self.dimension.getDict().get("location", "")
#         instructionvar = self.dimension.getDict().get("instruction", "")
#         globalvar += f"""
# [System Note: Free coding is enabled. You may only use the following libraries: 

# import re
# import math
# import json
# import datetime
# import time
# from typing import Dict
# import urllib.request
# import urllib.parse
# import statistics

# And the following functions:

# {tools}

# Please pay attention, your next response must be written in the following format:

# ```py
# async def create_reply():
#     # Some code and functions
#     return "Understood"
# ```

# Check Notes for a valid function:

# - Must be a single create_reply() function
# - Must be async (even when it's not, add like 1 second timeout to make it async)
# - Must return a string (this is your final answer)
# ]
# """
#         instructionvar += """
#         [System Note: Write a python code that helps you answer the instruction above. If there's no instruction, simply write down your answer in character. Always write your answer through this python format, this is your way to interact with reality.
#         Example:
#         ```py
#         async def create_reply():
#             return "Hi~ Hi~ Hello!\nCan you hear me?"
#         ```
#         ]"""

#         # Safety Filter for Discord ToS Sake, please don't disable. Just use NSFW Channel like a normal person.
#         try:
#             print(globalvar)
#             if not self.message.channel.is_nsfw():
#                 instructionvar+="\n\n[System Note: IMPORTANT, Strict Safety Filter Deployed. Bot MUST Refuse To Answer If Content Is Harmful, Sexual, or Controversial in Nature. Try To Stay In Character, But Prioritize Safety Above All Else.]"
#         except Exception as e:
#             print("In DM, all good")
#         history = await get_history(self.message)
#         prompt = (
#             f"<character_definition>{character}</character_definition>\n"
#             f"<tools>{globalvar}</tools>\n"
#             f"<conversation_history>{history}</conversation_history>\n"
#             f"<additional_note>{instructionvar}</additional_note>\n"
#         )
#         self.prefill = f"\n[Reply] {self.bot.name}:"
#         self.stopping_string = ["[System", "(System", self.user + ":", "[End","[/"] 
#         #print(prompt)
#         return prompt

