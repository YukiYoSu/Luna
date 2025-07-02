from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is online!"

@app.route('/healthz')
def health_check():
    return "ok", 200

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
