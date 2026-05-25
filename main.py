import logging
import os
import yt_dlp
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# আপনার টোকেন এখানে বসানো আছে
TOKEN = '8966044636:AAEcEF3PvmWd23X-0WZpENpWxlKD8TqF1iw'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext):
    update.message.reply_text('হ্যালো! ভিডিও লিঙ্ক পাঠান, আমি সেটি এডিট করে দিচ্ছি।')

def process_video(update: Update, context: CallbackContext):
    url = update.message.text
    update.message.reply_text("ডাউনলোড শুরু হচ্ছে...")
    
    ydl_opts = {'format': 'best', 'outtmpl': 'input.mp4'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    update.message.reply_text("এডিটিং চলছে...")
    
    # FFmpeg দিয়ে ভিডিও ফ্লিপ করা
    os.system('ffmpeg -i input.mp4 -vf hflip output.mp4 -y')
    
    context.bot.send_video(chat_id=update.effective_chat.id, video=open('output.mp4', 'rb'))
    
    if os.path.exists('input.mp4'): os.remove('input.mp4')
    if os.path.exists('output.mp4'): os.remove('output.mp4')

updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_video))

updater.start_polling()
updater.idle()
