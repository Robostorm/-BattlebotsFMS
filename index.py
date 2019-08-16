from flask import Flask, render_template
from flask_socketio import SocketIO
import vmix

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

# vMix Config
ipaddr = '192.168.2.212'
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




# SocketIO Match Play

@socketio.on('preStartClicked')
def preStartClicked():
    print ('Prestart!')
    # New teams should be pushed to Match Preview & Scoreboard here

@socketio.on('setAudienceDisplayClicked')
def setAudienceDisplayClicked():
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


# Scoring Page

redCornerBalloon1 = 1
redCornerBalloon2 = 1
blueCornerBalloon1 = 1
blueCornerBalloon2 = 1
redRobot1Balloon = 2
redRobot2Balloon = 2
blueRobot1Balloon = 2
blueRobot2Balloon = 2
redPenalty = 0
bluePenalty = 0


@socketio.on('redRobot1BalloonClicked')
def redRobot1BalloonClicked():
    print('redRobot1BalloonClicked')
    global redRobot1Balloon
    if redRobot1Balloon > 0:
        redRobot1Balloon = redRobot1Balloon - 1
    else:
        redRobot1Balloon = 2
    socketio.emit('updateImage', {'balloonID' : 'redRobot1BalloonImage', 'value' : redRobot1Balloon, 'color' : 'red'}, broadcast=True)
    print(redRobot1Balloon)

#@socketio.on('connect')
#def connect():
#    print('Hello')
#    socketio.emit('updateImage', {'balloonID' : 'redRobot1BalloonImage', 'value' : redRobot1Balloon, 'color' : 'red'}, broadcast=True)
#    socketio.emit('updateImage', {'balloonID' : 'redRobot2BalloonImage', 'value' : redRobot2Balloon, 'color' : 'red'}, broadcast=True)
#    socketio.emit('updateImage', {'balloonID' : 'blueRobot1BalloonImage', 'value' : blueRobot1Balloon, 'color' : 'blue'}, broadcast=True)
#    socketio.emit('updateImage', {'balloonID' : 'blueRobot2BalloonImage', 'value' : blueRobot2Balloon, 'color' : 'blue'}, broadcast=True)






if __name__ == '__main__':
    socketio.run(app, debug=True)