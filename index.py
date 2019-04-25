from flask import Flask, render_template
from flask_socketio import SocketIO
import vmix

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/match-play')
def matchPlay():
    return render_template('matchPlay.html')

@app.route('/robot-manager')
def robotManager():
    return render_template('robotManager.html')

@app.route('/event-manager')
def eventManager():
    return render_template('eventManager.html')

@app.route('/scoring')
def scoring():
    return render_template('scoring.html')



@socketio.on('startClicked')
def startClicked():
    print('Match Started!')
    #socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)

#if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0')
