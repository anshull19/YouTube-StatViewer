# app.py

from flask import Flask, render_template, request
import youtube_api

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/process', methods=['POST'])
def process():
    channel_id = request.form['channel_id']
    channel_info = youtube_api.get_channel_info(channel_id)
    popular_video_info = youtube_api.get_most_popular_video(channel_id)
    latest_video_info = youtube_api.get_latest_video(channel_id)

    if channel_info:
        return render_template('dashboard.html', channel_info=channel_info, most_popular_video=popular_video_info, latest_videos=latest_video_info)
    else:
        error_message = 'Error: Could not retrieve channel information. Please check the channel ID.'
        return render_template('dashboard.html', error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
