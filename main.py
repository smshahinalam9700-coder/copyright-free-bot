import logging
import os
import yt_dlp
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# আপনার টোকেনটি এখানে বসান
TOKEN = '8966044636:AAEcEF3PvmWd23X-0WZpENpWxlKD8TqF1iw'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext):
    update.message.reply_text('বট প্রস্তুত! ভিডিও লিঙ্ক পাঠান।')

def process_video(update: Update, context: CallbackContext):
    url = update.message.text
    update.message.reply_text("ডাউনলোড শুরু হচ্ছে...")
    
    # ইনপুট ফাইল এবং আউটপুট ফাইল ক্লিন রাখা
    if os.path.exists('input.mp4'): os.remove('input.mp4')
    if os.path.exists('output.mp4'): os.remove('output.mp4')
    
    ydl_opts = {'format': 'best', 'outtmpl': 'input.mp4'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        update.message.reply_text("এডিটিং চলছে, একটু অপেক্ষা করুন...")
        
        # দ্রুত এডিটিং কমান্ড (সিস্টেম ক্র্যাশ এড়াতে অপ্টিমাইজড)
        cmd = 'ffmpeg -i input.mp4 -vf "hflip,zoompan=z=1.05:d=1" -af "asetrate=44100*1.05" -preset ultrafast output.mp4 -y'
        os.system(cmd)
        
        if os.path.exists('output.mp4'):
            context.bot.send_video(chat_id=update.effective_chat.id, video=open('output.mp4', 'rb'))
        else:
            update.message.reply_text("এডিটিং ব্যর্থ হয়েছে।")
            
    except Exception as e:
        update.message.reply_text(f"ত্রুটি: {str(e)}")
    
    # সবশেষে ফাইল ডিলিট
    if os.path.exists('input.mp4'): os.remove('input.mp4')
    if os.path.exists('output.mp4'): os.remove('output.mp4')

# বট রান করা
updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_video))

# পোলিং স্টার্ট
updater.start_polling()
updater.idle()
