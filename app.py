from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os
import uuid
import threading
import time

app = Flask(__name__)

# HTML template
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Personal Video Downloader</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #6dd5ed, #2193b0);
            color: #fff;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        header {
            background-color: rgba(0, 0, 0, 0.3);
            padding: 20px;
            font-size: 28px;
            font-weight: bold;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        form {
            margin-top: 80px;
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 12px;
            display: inline-block;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        input {
            padding: 12px;
            width: 350px;
            border: none;
            border-radius: 6px;
            margin-right: 10px;
            font-size: 16px;
        }
        button {
            padding: 12px 25px;
            background-color: #ff9800;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            color: #fff;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        button:hover {
            background-color: #e68900;
        }
        footer {
            margin-top: 100px;
            padding: 15px;
            font-size: 14px;
            background: rgba(0, 0, 0, 0.3);
            position: fixed;
            width: 100%;
            bottom: 0;
        }
    </style>
</head>
<body>
    <header>🎥 Personal Video Downloader</header>
    <form action="/download" method="POST">
        <input type="url" name="url" placeholder="Paste video URL here" required>
        <button type="submit">Download</button>
    </form>
    <footer>Developed by Kemawilly</footer>
</body>
</html>
"""

def delete_file_later(filename, delay=2):
    """Delete file after a short delay (to avoid Windows file lock issues)."""
    def delayed_delete():
        time.sleep(delay)
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"Deleted: {filename}")
            except Exception as e:
                print(f"Error deleting {filename}: {e}")
    threading.Thread(target=delayed_delete, daemon=True).start()

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_PAGE)

@app.route("/download", methods=["POST"])
def download_video():
    video_url = request.form.get("url")
    unique_filename = f"video_{uuid.uuid4().hex}.mp4"

    ydl_opts = {
        "outtmpl": unique_filename,
        "format": "bestvideo+bestaudio/best"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # Schedule file deletion after sending
    delete_file_later(unique_filename, delay=3)

    return send_file(unique_filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
