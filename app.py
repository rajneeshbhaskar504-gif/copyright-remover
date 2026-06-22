import os
import subprocess
from flask import Flask, request, send_file, render_template_string

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Copyright Shield</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 50px 20px; background: #121212; color: white; }
        .box { border: 2px dashed #00ffd2; padding: 30px; border-radius: 10px; max-width: 400px; margin: auto; }
        input[type="file"] { margin: 20px 0; color: white; }
        button { background: #00ffd2; color: black; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <h2>🚀 Copyright Shield Dashboard</h2>
    <p>Upload video to bypass automated content ID filters</p>
    <div class="box">
        <form method="post" enctype="multipart/form-data" action="/process">
            <input type="file" name="video" accept="video/*" required><br>
            <button type="submit">Remove Copyright Signals</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/process', methods=['POST'])
def process_video():
    if 'video' not in request.files: return "No file uploaded", 400
    file = request.files['video']
    if file.filename == '': return "No file selected", 400

    input_path = os.path.join(app.config['UPLOAD_FOLDER'], "input_temp.mp4")
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], "output_shielded.mp4")
    file.save(input_path)

    # Fast processing optimized for cloud deployment
    ffmpeg_cmd = [
        'ffmpeg', '-y', '-i', input_path,
        '-vf', 'hflip,scale=1280:720,setpts=0.99*PTS',
        '-af', 'asetrate=44100*1.01,atescale=1/1.01,volume=1.05',
        '-c:v', 'libx264', '-crf', '28', '-preset', 'superfast', '-c:a', 'aac',
        '-map_metadata', '-1', output_path
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True)
        if os.path.exists(input_path): os.remove(input_path)
        return send_file(output_path, as_attachment=True, download_name="shielded_video.mp4")
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
