from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
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

@socketio.on('startMatch')
def handle_my_custom_event(json):
    print('Clicked!')

if __name__ == '__main__':
    socketio.run(app, host='192.168.56.5')

#if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0')
