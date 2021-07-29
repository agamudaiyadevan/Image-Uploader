import os
import uuid
import shutil
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from creds import Credentials
from telegraph import upload_file

logging.basicConfig(level=logging.INFO)


TGraph = Client(
    "Image upload bot",
    bot_token=Credentials.BOT_TOKEN,
    api_id=Credentials.API_ID,
    api_hash=Credentials.API_HASH,
)


@TGraph.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        text=f"Hello {message.from_user.first_name}!\n<b>I am Telegram to telegra.ph Image Uploader Bot</b>\n\n▷ Just give me a media under 5MB.\n▷ Then I will download it.\n▷ I will then upload it to the telegra.ph link.",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="TENDKOTTA", url=f"https://telegram.me/tendkotta"), InlineKeyboardButton(text="TharamaanaMovies", url=f"https://telegram.me/tharamaanamovies"), ],
                                           [InlineKeyboardButton(text="Youtube DL", url=f"https://telegram.me/YouTubedownloadergroup1"), InlineKeyboardButton(text="Channel List 📢", url=f"https://telegram.mr/tharamaanateambot"), InlineKeyboardButton(text="Bot Lists 🤖", url=f"https://telegram.me/tharamaanateambot"),],
                                           [InlineKeyboardButton(text="🤖 Movie Request Bot 🤖", url=f"https://telegram.me/Movie_Request_v3_Robot")]])
        )


@TGraph.on_message(filters.photo)
async def getimage(client, message):
    tmp = os.path.join("downloads", str(message.chat.id))
    if not os.path.isdir(tmp):
        os.makedirs(tmp)
    img_path = os.path.join(tmp, str(uuid.uuid4()) + ".jpg")
    dwn = await message.reply_text("<b>Downloading to my server...</b>", True)
    img_path = await client.download_media(message=message, file_name=img_path)
    await dwn.edit_text("<code>Uploading as telegra.ph link...</code>")
    try:
        tlink = upload_file(img_path)
    except Exception as error:
        await dwn.edit_text(f"<b>Oops something went wrong\n Please ▷Contact @TharamaanaAdmin.</b>")
        return
    await dwn.edit_text(
        text=f"<b>Link :-</b> <code>https://telegra.ph{tlink[0]}</code>,\n\n<b>▷ Please Subscribe</b> ❤️ [@TENDKOTTA](https://t.me/TENDKOTTA)",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="🔗 Open Link", url=f"https://telegra.ph{tlink[0]}"), InlineKeyboardButton(text="Share Link 👥", url=f"https://telegram.me/share/url?url=https://telegra.ph{tlink[0]}"), ],
                                           [InlineKeyboardButton(text="🤖 Movie Request Bot 🤖", url="https://telegram.me/movie_request_v3_robot")]])
        )
    shutil.rmtree(tmp, ignore_errors=True)


TGraph.run()
