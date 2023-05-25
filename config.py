import os
import dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

dotenv.load_dotenv('.env')

api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
string_session = os.environ.get('STRING_SESSION')
bot_token = os.environ.get('BOT_TOKEN')
main_bot_id = int(os.environ.get("BOT_ID"))

bot = TelegramClient('bot',api_id,api_hash).start(bot_token=bot_token)

client = TelegramClient(StringSession(string_session), api_id, api_hash)
