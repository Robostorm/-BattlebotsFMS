from flask import Flask, render_template
from flask_socketio import SocketIO
import vmix

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@socketio.on('startClicked')
def startClicked():
    print('Match Started!')
    #socketio.emit('my response', json, callback=messageReceived)