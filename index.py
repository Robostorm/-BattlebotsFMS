from flask import Flask, render_template, request
from flask_socketio import SocketIO
import vmix
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

driverRed1Name = 'Red 1'
driverRed2Name = 'Red 2'
driverBlue1Name = 'Blue 1'
driverBlue2Name = 'Blue 2'


# vMix Config
ipaddr = '192.168.50.6'
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

@app.route('/event-manager', methods=['GET', 'POST'])
def eventManager():
    global driverRed1Name
    global driverRed2Name
    global driverBlue1Name
    global driverBlue2Name
    driverRed1Name = request.args.get('driver1name')
    driverRed2Name = request.args.get('driver2name')
    driverBlue1Name = request.args.get('driver3name')
    driverBlue2Name = request.args.get('driver4name')
    return render_template('eventManager.html')

@app.route('/scoring')
def scoring():
    return render_template('scoring.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/setdrivernames', methods=['GET', 'POST'])
def setdrivernames():
    return 'hello'


gameClock = 120
gameActive = False
# Set to true to take down after match
takedownScoreboard = False



# Match Timer
def matchTimer():
    global gameClock
    global gameActive
    global takedownScoreboard
    threading.Timer(1.0, matchTimer).start()
    if gameActive:
        if gameClock > 0:
            gameClock = gameClock - 1
            calculateScores()
            vmix.set_red_score(redScore, _url)
            vmix.set_blue_score(blueScore, _url)
            socketio.emit('setScores', {'redScore' : redScore, 'blueScore' : blueScore}, broadcast=True)
            print(gameClock)
            takedownScoreboard = True
            if redScore == 26 or blueScore == 26:
                gameClock = 0
        else:
            gameActive = False
            calculateScores()
            calculateFinalScores()
            socketio.emit('setScores', {'redScore' : redScore, 'blueScore' : blueScore}, broadcast=True)
            if takedownScoreboard == True:
                vmix.overlay_scoreboard_out(_url)
                takedownScoreboard = False
            





matchTimer()

blueScore = 0
redScore = 0

#Calculate live scores (no bonuses)
def calculateScores():
    global blueScore
    global redScore
    # Calc blue score
    blueScore = (4 - redRobot1Balloon - redRobot2Balloon ) * 5 + (2 - redCornerBalloon1 - redCornerBalloon2) * 3
    # Calc red score
    redScore = (4 - blueRobot1Balloon - blueRobot2Balloon ) * 5 + (2 - blueCornerBalloon1 - blueCornerBalloon2) * 3

# Calc final scores with bonuses and penalties
def calculateFinalScores():
    blueBonus = 0
    redBonus = 0
    global blueScore
    global redScore
    if (redRobot1Balloon + redRobot2Balloon) == 4:
        redBonus += 5
    if (redRobot1Balloon + redRobot2Balloon + redCornerBalloon1 + redCornerBalloon2) == 6:
        redBonus +=2
    if (blueRobot1Balloon + blueRobot2Balloon) == 4:
        blueBonus += 5
    if (blueRobot1Balloon + blueRobot2Balloon + blueCornerBalloon1 + blueCornerBalloon2) == 6:
        blueBonus +=2
    calculateScores()
    redScore += redBonus + bluePenalty
    blueScore += blueBonus + redPenalty

# SocketIO Match Play
@socketio.on('preStartClicked')
def preStartClicked():
    print ('Prestart!')
    # New teams should be pushed to Match Preview & Scoreboard here
    global gameClock
    gameClock = 120
    vmix.set_red1_preview(driverRed1Name, _url)
    vmix.set_red2_preview(driverRed2Name, _url)
    vmix.set_blue1_preview(driverBlue1Name, _url)
    vmix.set_blue2_preview(driverBlue2Name, _url)
    vmix.set_red_score(0, _url)
    vmix.set_blue_score(0, _url)
    socketio.emit('setNames', {'red1Name' : driverRed1Name, 'red2Name' : driverRed2Name, 'blue1Name' : driverBlue1Name, 'blue2Name' : driverBlue2Name}, broadcast=True)
    

@socketio.on('setAudienceDisplayClicked')
def setAudienceDisplayClicked():
    vmix.overlay_match_preview_in(_url)
    print('Set Audience Display!')

@socketio.on('setLiveViewClicked')
def setLiveViewClicked():
    vmix.overlay_match_preview_out(_url)
    vmix.overlay_scoreboard_in(_url)
    print('Set Live View!')

@socketio.on('startMatchClicked')
def startClicked():
    global gameActive
    print('Match Started!')
    gameActive = True
    vmix.stop_game_clock(_url)
    vmix.set_game_clock('00:02:00', _url)
    vmix.start_game_clock(_url)
    

@socketio.on('commitMatchClicked')
def commitMatchClicked():
    print('Match Commit!')
    #Send final scores to scoreboard
    calculateFinalScores()
    socketio.emit('setScores', {'redScore' : redScore, 'blueScore' : blueScore}, broadcast=True)
    vmix.set_red_final_score(redScore, _url)
    vmix.set_blue_final_score(blueScore, _url)
    vmix.set_red1_result(driverRed1Name, _url)
    vmix.set_red2_result(driverRed2Name, _url)
    vmix.set_blue1_result(driverBlue1Name, _url)
    vmix.set_blue2_result(driverBlue2Name, _url)
    

    # Reset for next match
    global redCornerBalloon1
    global redCornerBalloon2
    global blueCornerBalloon1
    global blueCornerBalloon2
    global redRobot1Balloon
    global redRobot2Balloon
    global blueRobot1Balloon
    global blueRobot2Balloon
    global redPenalty
    global bluePenalty
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

    socketio.emit('updateImage', {'balloonID' : 'redRobot1BalloonImage', 'value' : redRobot1Balloon, 'color' : 'red', 'balloonNum' : '2'}, broadcast=True)
    socketio.emit('updateImage', {'balloonID' : 'redRobot2BalloonImage', 'value' : redRobot2Balloon, 'color' : 'red', 'balloonNum' : '2'}, broadcast=True)
    socketio.emit('updateImage', {'balloonID' : 'redCornerBalloon1Image', 'value' : redCornerBalloon1, 'color' : 'red', 'balloonNum' : '1'}, broadcast=True)
    socketio.emit('updateImage', {'balloonID' : 'redCornerBalloon2Image', 'value' : redCornerBalloon2, 'color' : 'red', 'balloonNum' : '1'}, broadcast=True)
    socketio.emit('updateImage', {'balloonID' : 'blueRobot1BalloonImage', 'value' : blueRobot1Balloon, 'color' : 'blue', 'balloonNum' : '2'}, broadcast=True)
    socketio.emit('updateImage', {'balloonID' : 'blueRobot2BalloonImage', 'value' : blueRobot2Balloon, 'color' : 'blue', 'balloonNum' : '2'}, broadcast=True)
    socketio.emit('updateImage', {'balloonID' : 'blueCornerBalloon1Image', 'value' : blueCornerBalloon1, 'color' : 'blue', 'balloonNum' : '1'}, broadcast=True)
    socketio.emit('updateImage', {'balloonID' : 'blueCornerBalloon2Image', 'value' : blueCornerBalloon2, 'color' : 'blue', 'balloonNum' : '1'}, broadcast=True)
    vmix.set_red_score(0,_url)
    vmix.set_blue_score(0,_url)
    socketio.emit('setScores', {'redScore' : 0, 'blueScore' : 0}, broadcast=True)

@socketio.on('postScoresClicked')
def postScoresClicked():
    print('Scores R up!')
    vmix.overlay_scoreboard_out(_url)
    vmix.overlay_match_result_in(_url)


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
    #print('redRobot1BalloonClicked')
    global redRobot1Balloon
    if redRobot1Balloon > 0:
        redRobot1Balloon = redRobot1Balloon - 1
    else:
        redRobot1Balloon = 2
    socketio.emit('updateImage', {'balloonID' : 'redRobot1BalloonImage', 'value' : redRobot1Balloon, 'color' : 'red', 'balloonNum' : '2'}, broadcast=True)
    #print(redRobot1Balloon)

@socketio.on('redRobot2BalloonClicked')
def redRobot2BalloonClicked():
    #print('redRobot2BalloonClicked')
    global redRobot2Balloon
    if redRobot2Balloon > 0:
        redRobot2Balloon = redRobot2Balloon - 1
    else:
        redRobot2Balloon = 2
    socketio.emit('updateImage', {'balloonID' : 'redRobot2BalloonImage', 'value' : redRobot2Balloon, 'color' : 'red', 'balloonNum' : '2'}, broadcast=True)
    #print(redRobot1Balloon)

@socketio.on('redCornerBalloon1Clicked')
def redCornerBalloon1Clicked():
    #print('redRobot1BalloonClicked')
    global redCornerBalloon1
    if redCornerBalloon1 > 0:
        redCornerBalloon1 = redCornerBalloon1 - 1
    else:
        redCornerBalloon1 = 1
    socketio.emit('updateImage', {'balloonID' : 'redCornerBalloon1Image', 'value' : redCornerBalloon1, 'color' : 'red', 'balloonNum' : '1'}, broadcast=True)
    #print(redRobot1Balloon)

@socketio.on('redCornerBalloon2Clicked')
def redCornerBalloon2Clicked():
    #print('redRobot1BalloonClicked')
    global redCornerBalloon2
    if redCornerBalloon2 > 0:
        redCornerBalloon2 = redCornerBalloon2 - 1
    else:
        redCornerBalloon2 = 1
    socketio.emit('updateImage', {'balloonID' : 'redCornerBalloon2Image', 'value' : redCornerBalloon2, 'color' : 'red', 'balloonNum' : '1'}, broadcast=True)
    #print(redRobot1Balloon)

@socketio.on('blueRobot1BalloonClicked')
def blueRobot1BalloonClicked():
    #print('blueRobot1BalloonClicked')
    global blueRobot1Balloon
    if blueRobot1Balloon > 0:
        blueRobot1Balloon = blueRobot1Balloon - 1
    else:
        blueRobot1Balloon = 2
    socketio.emit('updateImage', {'balloonID' : 'blueRobot1BalloonImage', 'value' : blueRobot1Balloon, 'color' : 'blue', 'balloonNum' : '2'}, broadcast=True)
    #print(blueRobot1Balloon)

@socketio.on('blueRobot2BalloonClicked')
def blueRobot2BalloonClicked():
    #print('blueRobot2BalloonClicked')
    global blueRobot2Balloon
    if blueRobot2Balloon > 0:
        blueRobot2Balloon = blueRobot2Balloon - 1
    else:
        blueRobot2Balloon = 2
    socketio.emit('updateImage', {'balloonID' : 'blueRobot2BalloonImage', 'value' : blueRobot2Balloon, 'color' : 'blue', 'balloonNum' : '2'}, broadcast=True)
    #print(blueRobot1Balloon)

@socketio.on('blueCornerBalloon1Clicked')
def blueCornerBalloon1Clicked():
    #print('blueRobot1BalloonClicked')
    global blueCornerBalloon1
    if blueCornerBalloon1 > 0:
        blueCornerBalloon1 = blueCornerBalloon1 - 1
    else:
        blueCornerBalloon1 = 1
    socketio.emit('updateImage', {'balloonID' : 'blueCornerBalloon1Image', 'value' : blueCornerBalloon1, 'color' : 'blue', 'balloonNum' : '1'}, broadcast=True)
    #print(blueRobot1Balloon)

@socketio.on('blueCornerBalloon2Clicked')
def blueCornerBalloon2Clicked():
    #print('blueRobot1BalloonClicked')
    global blueCornerBalloon2
    if blueCornerBalloon2 > 0:
        blueCornerBalloon2 = blueCornerBalloon2 - 1
    else:
        blueCornerBalloon2 = 1
    socketio.emit('updateImage', {'balloonID' : 'blueCornerBalloon2Image', 'value' : blueCornerBalloon2, 'color' : 'blue', 'balloonNum' : '1'}, broadcast=True)
    #print(blueRobot1Balloon)

@socketio.on('redPenaltyIncrease')
def redPenaltyIncrease():
    global redPenalty
    redPenalty += 1
    socketio.emit('setPenalties', {'red' : redPenalty, 'blue' : bluePenalty}, broadcast=True)
@socketio.on('redPenaltyDecrease')
def redPenaltyDecrease():
    global redPenalty
    redPenalty -= 1
    socketio.emit('setPenalties', {'red' : redPenalty, 'blue' : bluePenalty}, broadcast=True)
@socketio.on('bluePenaltyIncrease')
def bluePenaltyIncrease():
    global bluePenalty
    bluePenalty += 1
    socketio.emit('setPenalties', {'red' : redPenalty, 'blue' : bluePenalty}, broadcast=True)
@socketio.on('bluePenaltyDecrease')
def bluePenaltyDecrease():
    global bluePenalty
    bluePenalty -= 1
    socketio.emit('setPenalties', {'red' : redPenalty, 'blue' : bluePenalty}, broadcast=True)


#@socketio.on('balloonClicked')
#def balloonClicked(data):
#    print(data.balloonID)

@socketio.on('connect')
def connect():
    print('Hello')
    socketio.emit('updateImage', {'balloonID' : 'redRobot1BalloonImage', 'value' : redRobot1Balloon, 'color' : 'red', 'balloonNum' : '2'}, broadcast=True)
    socketio.emit('updateImage', {'balloonID' : 'redRobot2BalloonImage', 'value' : redRobot2Balloon, 'color' : 'red', 'balloonNum' : '2'}, broadcast=True)
    socketio.emit('updateImage', {'balloonID' : 'redCornerBalloon1Image', 'value' : redCornerBalloon1, 'color' : 'red', 'balloonNum' : '1'}, broadcast=True)
    socketio.emit('updateImage', {'balloonID' : 'redCornerBalloon2Image', 'value' : redCornerBalloon2, 'color' : 'red', 'balloonNum' : '1'}, broadcast=True)
    socketio.emit('updateImage', {'balloonID' : 'blueRobot1BalloonImage', 'value' : blueRobot1Balloon, 'color' : 'blue', 'balloonNum' : '2'}, broadcast=True)
    socketio.emit('updateImage', {'balloonID' : 'blueRobot2BalloonImage', 'value' : blueRobot2Balloon, 'color' : 'blue', 'balloonNum' : '2'}, broadcast=True)
    socketio.emit('updateImage', {'balloonID' : 'blueCornerBalloon1Image', 'value' : blueCornerBalloon1, 'color' : 'blue', 'balloonNum' : '1'}, broadcast=True)
    socketio.emit('updateImage', {'balloonID' : 'blueCornerBalloon2Image', 'value' : blueCornerBalloon2, 'color' : 'blue', 'balloonNum' : '1'}, broadcast=True)
    socketio.emit('setNames', {'red1Name' : driverRed1Name, 'red2Name' : driverRed2Name, 'blue1Name' : driverBlue1Name, 'blue2Name' : driverBlue2Name}, broadcast=True)
    socketio.emit('setPenalties', {'red' : redPenalty, 'blue' : bluePenalty}, broadcast=True)


@socketio.on('setNames')
def setNames(data):
    global driver1Name
    global driver2Name
    global driver3Name
    global driver4Name
    driver1Name = data.driver1Name
    driver2Name = data.driver2Name
    driver3Name = data.driver3Name
    driver4Name = data.driver4Name




if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')