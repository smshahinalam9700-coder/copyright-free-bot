import os
import random
import logging
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from moviepy.editor import VideoFileClip, vfx, concatenate_videoclips

# হেলথ চেক সিস্টেম
class HealthCheckServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_health_server():
    server = HTTPServer(('0.0.0.0', int(os.environ.get('PORT', 8080))), HealthCheckServer)
    server.serve_forever()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = os.environ.get("BOT_TOKEN")

def download_video(url, download_path):
    ydl_opts = {'format': 'best', 'outtmpl': download_path, 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def edit_copyright_free(input_path, output_path):
    with VideoFileClip(input_path) as clip:
        edited = clip.fx(vfx.mirror_x).fx(vfx.lum_contrast, lum=2)
        duration = int(edited.duration)
        subclips = [edited.subclip(i, min(i+5, duration)) for i in range(0, duration, 5)]
        final_clip = concatenate_videoclips(subclips).fx(vfx.speedx, 1.02)
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)
        final_clip.close()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    status = await msg.reply_text("🔄 প্রসেসিং...")
    in_file = f"in_{msg.message_id}.mp4"
    out_file = f"out_{msg.message_id}.mp4"
    try:
        await asyncio.to_thread(download_video, msg.text, in_file)
        await asyncio.to_thread(edit_copyright_free, in_file, out_file)
        with open(out_file, 'rb') as f:
            await msg.reply_video(video=f, caption="✅ ডান!")
        await status.delete()
    except Exception as e:
        await status.edit_text(f"❌ এরর: {e}")
    finally:
        for f in [in_file, out_file]:
            if os.path.exists(f): os.remove(f)

if __name__ == '__main__':
    threading.Thread(target=run_health_server, daemon=True).start()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()
