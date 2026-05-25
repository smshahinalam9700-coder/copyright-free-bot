import logging
import os
import yt_dlp
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# আপনার বটের টোকেন
TOKEN = '8966044636:AAEcEF3PvmWd23X-0WZpENpWxlKD8TqF1iw'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext):
    update.message.reply_text('বট প্রস্তুত! যেকোনো ভিডিও লিঙ্ক পাঠান, আমি সেটিকে কপিরাইট-মুক্ত করে এডিট করে দিচ্ছি।')

def process_video(update: Update, context: CallbackContext):
    url = update.message.text
    update.message.reply_text("ডাউনলোড শুরু হচ্ছে... দয়া করে অপেক্ষা করুন।")
    
    # ভিডিও ডাউনলোডের অপশন
    ydl_opts = {'format': 'best', 'outtmpl': 'input.mp4'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    update.message.reply_text("অ্যাডভান্সড এডিটিং চলছে (শেক, জুম, লোগো রিমুভ ও নয়েজ)...")
    
    # শক্তিশালী FFmpeg কমান্ড
    # -vf: হরাইজন্টাল ফ্লিপ, জুম-ইন, লোগো ব্লার, ভিডিও শেক
    # -af: অডিওতে নয়েজ এবং ইকো ইফেক্ট
    cmd = (
        'ffmpeg -i input.mp4 -vf "'
        'hflip, '
        'zoompan=z=\'min(zoom+0.001,1.2)\':d=125, '
        'delogo=x=10:y=10:w=100:h=50, '
        'rotate=1*PI/180" '
        '-af "aecho=0.8:0.9:1000:0.3, aformat=sample_rates=44100" '
        'output.mp4 -y'
    )
    
    os.system(cmd)
    
    # ফাইল পাঠানো
    if os.path.exists('output.mp4'):
        context.bot.send_video(chat_id=update.effective_chat.id, video=open('output.mp4', 'rb'))
        os.remove('output.mp4')
    else:
        update.message.reply_text("এডিটিংয়ে সমস্যা হয়েছে।")
    
    if os.path.exists('input.mp4'): os.remove('input.mp4')

updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_video))

updater.start_polling()
updater.idle()
