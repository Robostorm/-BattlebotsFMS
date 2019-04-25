from flask import Flask, render_template
from flask_socketio import SocketIO
import vmix

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

# vMix Config
ipaddr = '127.0.0.1'
def _url(path):
    return 'http://' + ipaddr + ':8088/api/?' + path

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

@app.route('/settings')
def settings():
    return render_template('settings.html')





@socketio.on('preStartClicked')
def preStartClicked():
    print ('Prestart!')

@socketio.on('setAudienceDisplayClicked')
def startClicked():
    resp = vmix.overlay_match_preview_in(_url)

@socketio.on('setLiveViewClicked')
def setLiveViewClicked():
    resp = vmix.overlay_match_preview_out(_url)
    resp = vmix.overlay_scoreboard_in(_url)

@socketio.on('startMatchClicked')
def startClicked():
    print('Match Started!')
    resp = vmix.stop_game_clock(_url)
    resp = vmix.set_game_clock('00:02:00', _url)
    resp = vmix.start_game_clock(_url)
    #socketio.emit('my response', json, callback=messageReceived)

@socketio.on('commitMatchClicked')
def commitMatchClicked():
    print('Match Commit!')

@socketio.on('postScoresClicked')
def postScoresClicked():
    print('Scores R up!')
    resp = vmix.overlay_scoreboard_out(_url)
    resp = vmix.overlay_match_result_in(_url)

if __name__ == '__main__':
    socketio.run(app, debug=True)