from flask import Flask, render_template
from flask_socketio import SocketIO
import TweepyFile as t

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.before_first_request
def your_function():
    t.runStream()

if __name__ == '__main__':
    socketio.run(app)
