from telegram.ext import ApplicationBuilder, ConversationHandler, CallbackQueryHandler, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os
import logger
import bot_logic
import settings_state_constants

# Access secret keys saved in .env file (telegram bot token obtained from bot father)
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_PORT = int(os.environ.get('PORT', os.getenv('WEBHOOK_PORT')))
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# Build the bot
bot = ApplicationBuilder().token(BOT_TOKEN).build()

logger.info("Successfully built the bot")

# Configure the bot with handlers that decide when to call the defined methods above
bot.add_handler(CommandHandler("help", bot_logic.help))

bot.add_handler(CommandHandler("hello", bot_logic.hello))

bot.add_handler(CommandHandler("cat", bot_logic.get_cat))

bot.add_handler(CommandHandler("breed", bot_logic.choose_breed))
bot.add_handler(CallbackQueryHandler(bot_logic.get_cat_with_breed))

settings_handler = ConversationHandler(
    entry_points = [CommandHandler("settings", bot_logic.set_user_settings)],
    states = {
        settings_state_constants.BREED: [MessageHandler(filters.Regex(bot_logic.get_cat_breeds_regex()), bot_logic.save_breed)],
        settings_state_constants.NO_OF_PHOTOS: [MessageHandler(filters.TEXT & filters.Regex("^([1-9]|10)$"), bot_logic.save_no_of_photos)],
        settings_state_constants.GIF: [MessageHandler(filters.TEXT & filters.Regex("^(GIF|Image)$"), bot_logic.save_is_gif)]
    },
    fallbacks = [CommandHandler("stop", bot_logic.stop)]
)
bot.add_handler(settings_handler)

bot.add_handler(CommandHandler("see_settings", bot_logic.see_settings))

# Start the bot
bot.run_webhook(listen = '0.0.0.0', port = WEBHOOK_PORT, url_path = BOT_TOKEN, webhook_url = WEBHOOK_URL + BOT_TOKEN)

logger.error("Bot has stopped running")