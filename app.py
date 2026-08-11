from flask import Flask, jsonify, request
from flask_cors import CORS
import yt_dlp
import re

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"status": "GitHub Codespaces YouTube Backend is running!"})

@app.route("/get-audio", methods=["GET"])
def get_youtube_audio():
    raw_url = request.args.get("url")
    if not raw_url:
        return jsonify({"error": "Parameter 'url' diperlukan"}), 400
    
    # Bersihkan URL dari parameter list/radio yang mengganggu
    url = raw_url.split("&")[0]
    
    try:
        ydl_opts = {
            'format': 'bestaudio',
            'noplaylist': True,  # Mencegah yt-dlp memuat playlist/radio
            'quiet': True,
            'cookiefile': 'cookies.txt',  # Pastikan file cookies.txt ada
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info.get('url', None)
            title = info.get('title', 'Unknown')
            
            if not audio_url:
                return jsonify({"error": "Gagal mengambil stream audio."}), 400
                
            return jsonify({
                "title": title,
                "audio_url": audio_url
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)