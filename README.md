# Cat-Telegram-Bot

Sends pictures of cats

## Description

Inspired by and adapted from a tutorial originally, but with modifications in structure and behavior. The end product code differs almost completely from the original tutorial's source code.

Listed are some of the enhancements that I worked on myself, without help from the tutorial:

1. Restructured the python files into modules to be exported, as well as added util files, instead of having it all in 1 file
1. Instead of manually hardcoding breeds of cats to choose from, I fetched all the breed data from the cat API and processed it
1. Implemented and organically integrated binary search, and other list algorithms (see `list_util.py`) into the project
1. Abstracted the logic and methods to form cleaner code
1. Implemented a Data Access Object (DAO) pattern
1. Implemented and incorporated logging
1. Implemented persistence with a Database Management System (MongoDB) instead of a JSON file saved locally
1. Deploying the bot

Try the bot out [here](https://t.me/cat_picture_bot)

**:exclamation: Note: Bot might take 20-30s to start up due to inactivity as it is being hosted on Heroku for free**

**:exclamation: Note: You will not be able to run the bot by simply pulling the source code. This GitHub Repo is just to allow users to try the bot by using the link above, as well as for reference to the source code**

## Commands

`/help`: Bot shows you all possible commands

`/hello`: Bot says hello

`/cat`: Bot sends a picture of a cat

`/breed`: Bot gives options of cat breeds to choose from. Once you choose a breed, Bot will send a cat picture of that breed

`/settings`: Allows user to specify breed of cat, number of photos at a time, and whether he / she wants GIFs or still images. (Only applies to the `/cat` command!)

`/stop`: If you were in the middle of setting your preferences using `/settings`, you could use this command to stop. However, any preferences indicated before you called this command would have been automatically saved.

## Things I Learnt / Improved in

- Telegram bot API
- Python in general (e.g. serialization & deserialization, data structures, lambda functions, classes, error handling and more)
- Asynchronous Programming
- Deploying a telegram bot
- Persistance in Python (JSON and MongoDB)
- Virtual Environment
- Debugging & Logging
  - Spent really long trying to figure out why pymongo could not connect to MongoDB Atlas. Turns out that some root CAs that MongoDB Atlas were using had expired, and thus I needed to manually install some certificates on my local machine. See [here](https://stackoverflow.com/questions/69397039/pymongo-ssl-certificate-verify-failed-certificate-has-expired-on-mongo-atlas). I found this error via logging in `DEBUG` mode.
