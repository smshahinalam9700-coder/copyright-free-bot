import os
import yt_dlp
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = 'YOUR_NEW_TOKEN_HERE'

def process_video(update, context):
    url = update.message.text
    update.message.reply_text("ডাউনলোড ও এডিটিং শুরু হচ্ছে...")
    
    # দ্রুত ডাউনলোডের জন্য format 18 (low quality for speed) ব্যবহার করুন
    ydl_opts = {'format': '18', 'outtmpl': 'input.mp4'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        # দ্রুত এডিটিং: হরাইজন্টাল ফ্লিপ এবং অডিও পিচ পরিবর্তন (কপিরাইট এড়াতে যথেষ্ট)
        cmd = 'ffmpeg -i input.mp4 -vf "hflip" -af "pitch=1.1" -preset ultrafast output.mp4 -y'
        os.system(cmd)
        
        if os.path.exists('output.mp4'):
            context.bot.send_video(chat_id=update.effective_chat.id, video=open('output.mp4', 'rb'))
        else:
            update.message.reply_text("এডিটিং ব্যর্থ হয়েছে।")
            
    except Exception as e:
        update.message.reply_text(f"ত্রুটি: {str(e)}")
    
    # ক্লিনআপ
    for f in ['input.mp4', 'output.mp4']:
        if os.path.exists(f): os.remove(f)

updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', lambda u, c: u.message.reply_text('লিঙ্ক পাঠান')))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_video))
updater.start_polling()
updater.idle()
