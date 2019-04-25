from flask import Flask, render_template
from flask_socketio import SocketIO
import vmix

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/fieldConfig')
def fieldConfig():
    return render_template('field.html')

@app.route('/scoring')
def scoring():
    return render_template('scoring.html')

@app.route('/connections')
def connections():
    return render_template('connections.html')

@socketio.on('startClicked')
def startClicked():
    print('Match Started!')
    #socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)

#if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0')
