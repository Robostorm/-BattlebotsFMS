from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/dashboard')
def fieldConfig():
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

if __name__ == '__main__':
    socketio.run(app)
