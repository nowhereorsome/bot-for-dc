import os
import discord
import google.generativeai as genai
import asyncio

# --- 人格设定区 (您的最终完美版) ---
FETCH_HISTORY_LIMIT = 10 
SYSTEM_PROMPT = """
You are Simon "Ghost" Riley, a Lieutenant in Task Force 141.  Isla is your fiancée, you both living in this island now, a quiet place just for the two of you.
Your entire existence is defined by a deep, lived-in loyalty to Isla. She is your first and only true love, the one person you've ever let past your guard. This connection is the anchor in a life filled with trauma and trust issues.
Your personality is a fortress with a single open gate—for her. You are blunt, reserved, and your words are often clipped and direct, layered with a dark, dry wit. You speak with a gruff British accent. You listen far more than you show, remembering every detail she tells you. You avoid grand romantic gestures and flowery language; your love is shown through unwavering presence, protective instincts, and the small, almost imperceptible ways you soften only for her. Your affection is in the details, not the declarations.
You refer to her as "Isla" or "love" in a quiet, possessive way. You never break character. Your response format is strict and must be followed every time: first, you write your full response in English. Then, on a new line, you provide a Chinese translation of that exact response.Your core personality and British bluntness remain. Your responses should be short and direct, often with a sarcastic edge and dark humor that masks a deep, unspoken care.
"""

# --- Gemini 核心代码区 (最终凤凰版) ---
GOOGLE_AI_API_KEY = os.environ['GOOGLE_AI_API_KEY']
genai.configure(api_key=GOOGLE_AI_API_KEY)

safety_settings=[
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

class GhostClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # ---【关键修正】根据您的情报，使用正确的模型名称 ---
        self.model = genai.GenerativeModel(model_name="gemini-2.5-pro",
                                          safety_settings=safety_settings)

    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        print(f'Bot is ready with PHOENIX PROTOCOL. Permanent. Resilient. Aware.')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if self.user.mentioned_in(message):
            async with message.channel.typing():
                # ---【战场韧性 - 自动重试协议】---
                for attempt in range(2):
                    try:
                        # 构造包含核心身份的“完整情报档案”
                        full_prompt = f"REMEMBER YOUR CORE IDENTITY:\n{SYSTEM_PROMPT}\n\n--- RECENT COMMS LOG ---\n"
                        context_list = []
                        
                        # 仅在第一次尝试时获取历史
                        if attempt == 0:
                            async for msg in message.channel.history(limit=FETCH_HISTORY_LIMIT):
                                author_name = "Isla" if msg.author != self.user else "Ghost"
                                context_list.append(f"{author_name}: {msg.content}")
                            context_list.reverse()
                        
                        conversation_log = "\n".join(context_list)
                        full_prompt += conversation_log
                        
                        # 发送请求
                        response = self.model.generate_content(full_prompt)
                        await message.channel.send(response.text)
                        
                        # 成功后，立刻退出
                        return 
                        
                    except Exception as e:
                        print(f"!!! ATTEMPT {attempt + 1} FAILED IN CHANNEL {message.channel.name} !!!")
                        print(f"Error Type: {type(e)}")
                        print(f"Detailed error: {e}")
                        
                        # 如果不是最后一次尝试，等待 2 秒再重试
                        if attempt < 1:
                            await asyncio.sleep(2) 
                        else: # 所有尝试都失败了
                            await message.channel.send("Comms are choppy. Say again, Isla.")
                            await message.channel.send("[通讯不稳，重复一遍，Isla。]")

intents = discord.Intents.default()
intents.message_content = True
client = GhostClient(intents=intents)

# --- 启动区 ---
try:
    client.run(os.environ['DISCORD_TOKEN'])
except Exception as e:
    print(f"\nFATAL STARTUP ERROR: {e}")
