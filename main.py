import os
import random
import logging
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from moviepy.editor import VideoFileClip, vfx

# ক্লাউড সার্ভার সচল রাখার জন্য হেলথ চেক সিস্টেম
class HealthCheckServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running perfectly!")

def run_health_server():
    server = HTTPServer(('0.0.0.0', int(os.environ.get('PORT', 8080))), HealthCheckServer)
    server.serve_forever()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# টোকেনটি ক্লাউড এনভায়রনমেন্ট থেকে অটোমেটিক সংগ্রহ করবে
TOKEN = os.environ.get("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")

# ১. সোশাল মিডিয়া থেকে ওয়াটারমার্ক ছাড়া ভিডিও ডাউনলোডার ইউনিট
def download_video(url, download_path):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': download_path,
        'noplaylist': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# ২. ডাইনামিক কপিরাইট ফ্রি এডিটিং ইউনিট (ক্রিকেট, গোপাল ভাঁড়, মুভির জন্য স্পেশাল)
def edit_copyright_free(input_path, output_path):
    with VideoFileClip(input_path) as clip:
        # র্যান্ডমাইজেশন মেকানিজম (যাতে অ্যালগরিদম প্যাটার্ন ধরতে না পারে)
        random_speed = random.choice([1.01, 1.02, 1.03])
        
        # ভিডিও ফ্লিপ এবং কালার টিউনিং
        edited = clip.fx(vfx.mirror_x)
        edited = edited.fx(vfx.lum_contrast, lum=random.choice([2, 3]), contrast=0.04)
        
        # ৫ সেকেন্ড পর পর অটো-কাট ও ডাইনামিক জুম মেকানিজম
        duration = int(edited.duration)
        clips = []
        for start in range(0, duration, 5):
            end = min(start + 5, duration)
            if end - start < 1:
                continue
            sub_clip = edited.subclip(start, end)
            
            # অল্টারনেট জুম-ইন এবং জুম-আউট এফেক্ট
            if (start // 5) % 2 == 0:
                sub_clip = sub_clip.fx(vfx.resize, lambda t: 1 + 0.01 * t) # আস্তে আস্তে জুম-ইন
            else:
                sub_clip = sub_clip.fx(vfx.resize, lambda t: 1.05 - 0.01 * t) # আস্তে আস্তে জুম-আউট
                
            clips.append(sub_clip)
            
        # সব ক্লিপ একসাথে জোড়া দেওয়া এবং অডিও-ভিডিও স্পিড ফিক্স করা
        from moviepy.editor import concatenate_videoclips
        final_clip = concatenate_videoclips(clips).fx(vfx.speedx, random_speed)
        
        # মেটাডেটা চিরতরে মুছে ফেলা
        final_clip.write_videofile(
            output_path, 
            codec="libx264", 
            audio_codec="aac",
            ffmpeg_params=["-map_metadata", "-1"], # মেটাডেটা ওয়াশ
            logger=None
        )
        final_clip.close()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    url = message.text or message.caption
    
    # ইউজার লিংক দিয়েছে নাকি সরাসরি ভিডিও আপলোড করেছে তা চেক করা
    is_url = url and (url.startswith("http://") or url.startswith("https://"))
    is_video = message.video or (message.document and message.document.mime_type.startswith('video/'))
    
    if not is_url and not is_video:
        await message.reply_text("❌ দয়া করে একটি সঠিক ভিডিও লিংক (FB, YT, TikTok) পাঠান অথবা সরাসরি মেমোরি থেকে ভিডিও আপলোড করুন।")
        return

    status = await message.reply_text("🔄 প্রসেসিং শুরু হয়েছে... মেটাডেটা ক্লিন ও ডাইনামিক এডিটিং চলছে।")
    input_file = f"in_{message.message_id}.mp4"
    output_file = f"out_{message.message_id}.mp4"

    try:
        if is_url:
            await status.edit_text("📥 সোশ্যাল মিডিয়া থেকে ওয়াটারমার্ক ছাড়া ভিডিও ডাউনলোড হচ্ছে...")
            await asyncio.to_thread(download_video, url, input_file)
        else:
            await status.edit_text("📥 আপনার আপলোড করা ভিডিওটি সার্ভারে নেওয়া হচ্ছে...")
            tg_file = await context.bot.get_file(message.video.file_id if message.video else message.document.file_id)
            await tg_file.download_to_drive(input_file)

        await status.edit_text("🎬 ৫ সেকেন্ড অটো-কাট, ডাইনামিক জুম এবং ক্যামেরা অ্যাঙ্গেল পরিবর্তন করা হচ্ছে...")
        await asyncio.to_thread(edit_copyright_free, input_file, output_file)

        await status.edit_text("🚀 এডিটিং সফল! ফাইল পাঠানো হচ্ছে...")
        with open(output_file, 'rb') as vf:
            await message.reply_video(video=vf, caption="✅ আপনার কপিরাইট ফ্রি ভিডিও প্রস্তুত।")
        await status.delete()

    except Exception as e:
        logging.error(e)
        await status.edit_text("❌ এই ফাইলটি প্রসেস করা সম্ভব হয়নি। লিংকটি চেক করুন অথবা অন্য ফাইল দিয়ে চেষ্টা করুন।")
    finally:
        for f in [input_file, output_file]:
            if os.path.exists(f):
                os.remove(f)

def main():
    threading.Thread(target=run_health_server, daemon=True).start()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT | filters.VIDEO | filters.Document.VIDEO, handle_message))
    print("Bot lives on Cloud...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
