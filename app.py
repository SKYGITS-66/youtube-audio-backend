from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from urllib.parse import unquote

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"status": "Cobalt Proxy YouTube Backend is running!"})

@app.route("/get-audio", methods=["GET"])
def get_youtube_audio():
    try:
        raw_url = request.args.get("url")
        if not raw_url:
            return jsonify({"error": "Parameter 'url' diperlukan"}), 400
        
        decoded_url = unquote(raw_url)
        
        cobalt_instances = [
            "https://co.wuk.sh/api/json",
            "https://cobalt.k8s.lu/api/json"
        ]

        payload = {
            "url": decoded_url,
            "isAudioOnly": True,
            "filenamePattern": "basic"
        }
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        audio_url = None
        for instance in cobalt_instances:
            try:
                res = requests.post(instance, json=payload, headers=headers, timeout=6)
                if res.status_code == 200:
                    data = res.json()
                    status = data.get("status")
                    
                    if status in ["stream", "redirect"]:
                        audio_url = data.get("url")
                        break
                    elif status == "picker":
                        picker = data.get("picker", [])
                        if picker and picker[0].get("url"):
                            audio_url = picker[0].get("url")
                            break
            except Exception:
                continue

        if not audio_url:
            return jsonify({"error": "Gagal mengambil stream dari server Cobalt."}), 500

        return jsonify({
            "title": "YouTube Audio Stream",
            "audio_url": audio_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)