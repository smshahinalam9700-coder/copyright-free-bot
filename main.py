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

# হেলথ চেক সিস্টেম
class HealthCheckServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running perfectly!")

def run_health_server():
    try:
        server = HTTPServer(('0.0.0.0', int(os.environ.get('PORT', 8080))), HealthCheckServer)
        server.serve_forever()
    except Exception as e:
        logging.error(f"Health server error: {e}")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.environ.get("BOT_TOKEN")

def download_video(url, download_path):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': download_path,
        'noplaylist': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def edit_copyright_free(input_path, output_path):
    with VideoFileClip(input_path) as clip:
        random_speed = random.choice([1.01, 1.02, 1.03])
        edited = clip.fx(vfx.mirror_x)
        edited = edited.fx(vfx.lum_contrast, lum=random.choice([2, 3]), contrast=0.04)
        
        duration = int(edited.duration)
        clips = []
        for start in range(0, duration, 5):
            end = min(start + 5, duration)
            if end - start < 1:
                continue
            sub_clip = edited.subclip(start, end)
            if (start // 5) % 2 == 0:
                sub_clip = sub_clip.fx(vfx.resize, lambda t: 1 + 0.01 * t)
            else:
                sub_clip = sub_clip.fx(vfx.resize, lambda t: 1.05 - 0.01 * t)
            clips.append(sub_clip)
            
        from moviepy.editor import concatenate_videoclips
        final_clip = concatenate_videoclips(clips).fx(vfx.speedx, random_speed)
        final_clip.write_videofile(
            output_path, 
            codec="libx264", 
            audio_codec="aac",
            ffmpeg_params=["-map_metadata", "-1"],
            logger=None
        )
        final_clip.close()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    message = update.message
    url = message.text or message.caption
    is_url = url and (url.startswith("http://") or url.startswith("https://"))
    is_video = message.video or (message.document and message.document.mime_type and message.document.mime_type.startswith('video/'))
    
    if not is_url and not is_video:
        await message.reply_text("❌ সঠিক লিংক বা ভিডিও দিন।")
        return

    status = await message.reply_text("🔄 প্রসেসিং শুরু হয়েছে...")
    input_file = f"in_{message.message_id}.mp4"
    output_file = f"out_{message.message_id}.mp4"

    try:
        if is_url:
            await asyncio.to_thread(download_video, url, input_file)
        else:
            file_id = message.video.file_id if message.video else message.document.file_id
            tg_file = await context.bot.get_file(file_id)
            await tg_file.download_to_drive(input_file)

        await asyncio.to_thread(edit_copyright_free, input_file, output_file)
        with open(output_file, 'rb') as vf:
            await message.reply_video(video=vf, caption="✅ প্রস্তুত!")
        await status.delete()
    except Exception as e:
        await status.edit_text("❌ সমস্যা হয়েছে।")
    finally:
        for f in [input_file, output_file]:
            if os.path.exists(f): 
                try: os.remove(f)
                except: pass

def main():
    if not TOKEN: return
    threading.Thread(target=run_health_server, daemon=True).start()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT | filters.VIDEO | filters.Document.VIDEO, handle_message))
    application.run_polling(close_loop=False, drop_pending_updates=True)

if __name__ == '__main__':
    main()
