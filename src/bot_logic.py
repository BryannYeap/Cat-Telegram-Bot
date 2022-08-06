from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ConversationHandler
import cat_api
import settings_state_constants
import list_util
from user_entity import User_Entity
import user_repository

# Defining methods that the bot can call

# /help

async def help(update, context):
    await update.message.reply_text('''
        
Here are some of the commands you can use!

/help  -  Bot shows you all possible commands

/hello  -  Bot says hello

/cat  -  Bot sends a picture of a cat

/breed  -  Bot gives options of cat breeds to choose from. Once you choose a breed, Bot will send a cat picture of that breed

/settings  -  Allows user to specify breed of cat, number of photos at a time, and whether he / she wants GIFs or still images. (Only applies to the /cat command!)

/stop  -  If you were in the middle of setting your preferences using /settings, you could use this command to stop. However, any preferences indicated before you called this command would have been automatically saved.

/see_settings -  Bot shows your preferred settings

If you want to find out more about this bot, head to https://github.com/BryannYeap/Cat-Telegram-Bot
Contact me at @BryannYeapKokKeong

    ''')

# /hello 

async def hello(update, context):
    # The update param contains all user info
    await update.message.reply_text(f'Hello {update.effective_user.first_name}!')

# /cat

async def get_cat(update, context):
    user = update.message.from_user
    
    if not user_repository.user_exists(user.id):
        cats = cat_api.get_cats('all', '1', False)
        url = cats[0]['url']
        await context.bot.send_photo(chat_id = update.effective_chat.id, photo = url)
    else: 
        user_entity = user_repository.get_user(user.id)
        cats = cat_api.get_cats(user_entity.breed, user_entity.no_of_photos, user_entity.is_gif)

        if not cats:
            await update.message.reply_text("Sorry! There are no cats for your settings :( Try changing them with /settings !")
            return

        for cat in cats:
            url = cat['url']
            if user_entity.is_gif:
                await context.bot.send_animation(chat_id=update.effective_chat.id, animation=url)
            else:
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)

        if len(cats) < int(user_entity.no_of_photos):
            await update.message.reply_text("Sorry, that's all the cats we could find!")

# /breed

async def choose_breed(update, context):
    keyboard = get_cat_breed_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose a breed: ", reply_markup = reply_markup)

def get_cat_breed_keyboard():
    cat_breeds = cat_api.get_cat_breeds()

    for cat_breed in range(len(cat_breeds)):
        cat_breeds[cat_breed] = InlineKeyboardButton(
            cat_breeds[cat_breed]['name'],
            callback_data = cat_breeds[cat_breed]['id']
        )
    
    cat_keyboard = list_util.two_dimension_listify(2, cat_breeds)
    return cat_keyboard

async def get_cat_with_breed(update, context):
    query = update.callback_query

    await query.answer() # Answer the query with nothing, if not, will result in some problems

    breed = query.data

    cats = cat_api.get_cats(breed, '1', False)
    url = cats[0]['url']
    await context.bot.send_photo(chat_id = update.effective_chat.id, photo = url)

# /settings

async def set_user_settings(update, context):
    user = update.message.from_user

    if not user_repository.user_exists(user.id):
        user_entity = User_Entity(user.id, user.username, user.first_name, 'all', '1', False)
        user_repository.add_user(user_entity)

    await set_breed(update)

    return settings_state_constants.BREED

async def set_breed(update):
    keyboard = [['All of them!']]
    cat_breed_keyboard = get_cat_breed_keyboard()
    for row in cat_breed_keyboard:
        for keyboard_button in range(len(row)):
            row[keyboard_button] = row[keyboard_button].text

    keyboard += cat_breed_keyboard

    await update.message.reply_text(
        "What is your favourite breed?",
        reply_markup = ReplyKeyboardMarkup(
            keyboard, one_time_keyboard = True, input_field_placeholder = "Favourite Breed?"
        )
    )

def get_cat_breeds_regex():
    cat_breeds = cat_api.get_cat_breeds()
    for cat_breed in range(len(cat_breeds)):
        cat_breeds[cat_breed] = cat_breeds[cat_breed]['name']
    return "^(All of them!|" + "|".join(cat_breeds) + ")$"

async def save_breed(update, context):
    user = update.message.from_user

    breed = update.message.text
    breed_id = cat_api.get_cat_breed_id_from_name(breed)

    user_entity = user_repository.get_user(user.id)
    user_entity.breed = breed_id
    user_repository.update_user(user.id, user_entity)

    await set_no_of_photos(update)

    return settings_state_constants.NO_OF_PHOTOS

async def set_no_of_photos(update):
    reply_keyboard = list_util.two_dimension_listify(5, list(map(lambda number : str(number), range(1,11))))

    await update.message.reply_text(
        "Sure! How many photos would you like at a time?",
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, input_field_placeholder = "How many photos?"
        )
    )

async def save_no_of_photos(update, context):
    user = update.message.from_user
    no_of_photos = update.message.text
    
    user_entity = user_repository.get_user(user.id)
    user_entity.no_of_photos = no_of_photos
    user_repository.update_user(user.id, user_entity)

    await set_is_gif(update)

    return settings_state_constants.GIF

async def set_is_gif(update):
    reply_keyboard = [['GIF', 'Image']]

    await update.message.reply_text(
        "Gotcha! Lastly, do you want GIFs or images?",
        reply_markup = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard = True, input_field_placeholder = "GIF or Image?"
        )
    )

async def save_is_gif(update, context):
    user = update.message.from_user
    is_gif = update.message.text == 'GIF'
    
    user_entity = user_repository.get_user(user.id)
    user_entity.is_gif = is_gif
    user_repository.update_user(user.id, user_entity)

    await finish_settings(update)

    return ConversationHandler.END

async def finish_settings(update):
    await update.message.reply_text(
        "Thanks! Your settings have successfully been saved!",
        reply_markup = ReplyKeyboardRemove()
    )

# /stop

async def stop(update, context):
    await update.message.reply_text(
        "Ok, we'll stop saving your settings! Note that any settings you have made up to this point would have been saved.",
        reply_markup = ReplyKeyboardRemove()
    )

    return ConversationHandler.END

# /see_settings

async def see_settings(update, context):
    user = update.message.from_user

    if not user_repository.user_exists(user.id):
        user_entity = User_Entity(user.id, user.username, user.first_name, 'all', '1', False)
        user_repository.add_user(user_entity)
    
    user_entity = user_repository.get_user(user.id)

    await update.message.reply_text(f'''

        These are your preferred settings!

Breed: {cat_api.get_cat_breed_from_breed_id(user_entity.breed)}

Number of images / gifs at a time: {user_entity.no_of_photos}

GIFs or Images: {'GIFs' if user_entity.is_gif else 'Images'} 

    ''')
