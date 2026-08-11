from flask import Flask, jsonify, request
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"status": "GitHub Codespaces YouTube Backend is running with Cookies!"})

@app.route("/get-audio", methods=["GET"])
def get_youtube_audio():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Parameter 'url' diperlukan"}), 400
    
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'cookiefile': 'cookies.txt', # <-- Menambahkan cookies agar tidak terdeteksi bot
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