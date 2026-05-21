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

# হেলথ চেক সার্ভার
class HealthCheckServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_health_server():
    server = HTTPServer(('0.0.0.0', int(os.environ.get('PORT', 8080))), HealthCheckServer)
    server.serve_forever()

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("BOT_TOKEN")

def download_video(url, download_path):
    ydl_opts = {'format': 'best', 'outtmpl': download_path, 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def edit_copyright_free(input_path, output_path):
    with VideoFileClip(input_path) as clip:
        # মিরর এবং ব্রাইটনেস ইফেক্ট
        edited = clip.fx(vfx.mirror_x).fx(vfx.lum_contrast, lum=2)
        
        # ক্লিপ এডিটিং
        duration = int(edited.duration)
        subclips = [edited.subclip(i, min(i+5, duration)) for i in range(0, duration, 5)]
        final_clip = concatenate_videoclips(subclips).fx(vfx.speedx, 1.02)
        
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)
        final_clip.close()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    msg = update.message
    url = msg.text
    
    status = await msg.reply_text("🔄 প্রসেসিং শুরু হয়েছে...")
    in_file = f"in_{msg.message_id}.mp4"
    out_file = f"out_{msg.message_id}.mp4"
    
    try:
        await asyncio.to_thread(
