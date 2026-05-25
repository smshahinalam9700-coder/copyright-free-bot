import logging
import os
import yt_dlp
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# আপনার প্রদান করা টোকেন এখানে যুক্ত করা হয়েছে
TOKEN = '8966044636:AAEcEF3PvmWd23X-0WZpENpWxlKD8TqF1iw'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext):
    update.message.reply_text('বট প্রস্তুত! যেকোনো ভিডিও লিঙ্ক পাঠান, আমি সেটিকে এডিট করে দিচ্ছি।')

def process_video(update: Update, context: CallbackContext):
    url = update.message.text
    update.message.reply_text("ডাউনলোড ও এডিটিং শুরু হচ্ছে, অপেক্ষা করুন...")
    
    # পুরনো ফাইল থাকলে ডিলিট করে নেওয়া
    for f in ['input.mp4', 'output.mp4']:
        if os.path.exists(f): os.remove(f)
    
    ydl_opts = {'format': 'best', 'outtmpl': 'input.mp4'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # দ্রুত এডিটিংয়ের জন্য অপ্টিমাইজড কমান্ড
        cmd = 'ffmpeg -i input.mp4 -vf "hflip,zoompan=z=1.05:d=1" -af "asetrate=44100*1.05" -preset ultrafast output.mp4 -y'
        os.system(cmd)
        
        if os.path.exists('output.mp4'):
            context.bot.send_video(chat_id=update.effective_chat.id, video=open('output.mp4', 'rb'))
        else:
            update.message.reply_text("এডিটিং সম্পন্ন হতে ব্যর্থ হয়েছে।")
            
    except Exception as e:
        update.message.reply_text(f"ত্রুটি হয়েছে: {str(e)}")
    
    # শেষে ফাইল ক্লিনআপ
    for f in ['input.mp4', 'output.mp4']:
        if os.path.exists(f): os.remove(f)

# বট ইনিশিয়ালাইজেশন
updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_video))

updater.start_polling()
updater.idle()
