from aiogram import Bot, types

# Load .env
import os
from dotenv import load_dotenv
load_dotenv()
    
# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.getenv('BOTTOKEN')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

bot = Bot(
    token=TOKEN,
    parse_mode='HTML'
)