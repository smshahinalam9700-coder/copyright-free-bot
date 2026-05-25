import os
import yt_dlp
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)

# আপনার বটের টোকেন (নিরাপত্তার জন্য এনভায়রনমেন্ট ভেরিয়েবল ব্যবহার করা উত্তম)
TOKEN = 'YOUR_NEW_TOKEN_HERE' 

def process_video(update, context):
    url = update.message.text
    update.message.reply_text("ডাউনলোড ও এডিটিং শুরু হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...")
    
    # দ্রুত ডাউনলোডের জন্য অপশন
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'input.mp4'
    }
    
    try:
        # ডাউনলোড
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        # শক্তিশালী এডিটিং কমান্ড (দ্রুত ও কপিরাইট ফ্রি)
        # হরাইজন্টাল ফ্লিপ, সামান্য জুম, অডিও পিচ পরিবর্তন এবং মেটাডাটা ক্লিনিং
        cmd = (
            'ffmpeg -i input.mp4 -vf "hflip,zoompan=z=1.05:d=1" '
            '-af "asetrate=44100*1.05,atempo=1/1.05" '
            '-preset ultrafast -c:v libx264 -crf 23 -c:a aac output.mp4 -y'
        )
        os.system(cmd)
        
        # ফাইল পাঠানো
        if os.path.exists('output.mp4'):
            context.bot.send_video(chat_id=update.effective_chat.id, video=open('output.mp4', 'rb'))
        else:
            update.message.reply_text("এডিটিং সম্পন্ন হতে ব্যর্থ হয়েছে।")
            
    except Exception as e:
        update.message.reply_text(f"একটি সমস্যা হয়েছে: {str(e)}")
    
    # ফাইল ক্লিনআপ
    for f in ['input.mp4', 'output.mp4']:
        if os.path.exists(f):
            os.remove(f)

# বট শুরু
updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', lambda u, c: u.message.reply_text('ভিডিও লিঙ্ক পাঠান')))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_video))

updater.start_polling()
updater.idle()
