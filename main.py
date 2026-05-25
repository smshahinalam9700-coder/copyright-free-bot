import logging
import os
import yt_dlp
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# আপনার টোকেনটি এখানে সঠিকভাবে বসানো হয়েছে
TOKEN = '8966044636:AAEcEF3PvmWd23X-0WZpENpWxlKD8TqF1iw'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext):
    update.message.reply_text('বট প্রস্তুত! ভিডিও লিঙ্ক পাঠান।')

def process_video(update: Update, context: CallbackContext):
    url = update.message.text
    update.message.reply_text("ডাউনলোড শুরু হচ্ছে...")
    
    # ফাইল ক্লিন রাখা
    for f in ['input.mp4', 'output.mp4']:
        if os.path.exists(f): os.remove(f)
    
    try:
        ydl_opts = {'format': 'best', 'outtmpl': 'input.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        update.message.reply_text("এডিটিং চলছে...")
        
        # অপ্টিমাইজড এবং হালকা কমান্ড
        cmd = 'ffmpeg -i input.mp4 -vf "hflip" -preset ultrafast output.mp4 -y'
        os.system(cmd)
        
        if os.path.exists('output.mp4'):
            context.bot.send_video(chat_id=update.effective_chat.id, video=open('output.mp4', 'rb'))
        else:
            update.message.reply_text("এডিটিং ব্যর্থ হয়েছে।")
            
    except Exception as e:
        update.message.reply_text(f"ত্রুটি: {str(e)}")
    
    # শেষে ফাইল ডিলিট
    for f in ['input.mp4', 'output.mp4']:
        if os.path.exists(f): os.remove(f)

updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_video))

updater.start_polling()
updater.idle()
