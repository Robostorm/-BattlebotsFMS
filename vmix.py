# vmix.py vMix Python Library for Battlebots
import requests

# Scoreboard texts & clock functions
def set_red_score(score, _url):
    return requests.get(_url('Function=SetText&Input=Scoreboard&SelectedName=Home Score.Text&Value={:d}'.format(score)))
def set_blue_score(score, _url):
    return requests.get(_url('Function=SetText&Input=Scoreboard&SelectedName=Away Score.Text&Value={:d}'.format(score)))
def set_game_clock(time, _url):
    return requests.get(_url('Function=SetCountdown&Input=Scoreboard&SelectedName=CLOCK.Text&Value={:s}'.format(time)))
def start_game_clock(_url):
    return requests.get(_url('Function=StartCountdown&Input=Scoreboard&SelectedName=CLOCK.Text'))
def stop_game_clock(_url):
    return requests.get(_url('Function=StopCountdown&Input=Scoreboard&SelectedName=CLOCK.Text'))
def pause_game_clock(_url):
    return requests.get(_url('Function=PauseCountdown&Input=Scoreboard&SelectedName=CLOCK.Text'))
def set_scoreboard_top_text(text, _url):
    return requests.get(_url('Function=SetText&Input=Scoreboard&SelectedName=Title 1.Text&Value={:s}'.format(text)))
def set_scoreboard_bottom_text(text, _url):
    return requests.get(_url('Function=SetText&Input=Scoreboard&SelectedName=Title 2.Text&Value={:s}'.format(text)))


# Overlays
def overlay_scoreboard_in(_url):
    return requests.get(_url('Function=OverlayInput1In&Input=Scoreboard'))
def overlay_scoreboard_out(_url):
    return requests.get(_url('Function=OverlayInput1Out&Input=Scoreboard'))
def overlay_match_preview_in(_url):
    return requests.get(_url('Function=OverlayInput2In&Input=MatchPreview'))
def overlay_match_preview_out(_url):
    return requests.get(_url('Function=OverlayInput2Out&Input=MatchPreview'))
def overlay_match_result_in(_url):
    return requests.get(_url('Function=OverlayInput2In&Input=MatchResult'))
def overlay_match_result_out(_url):
    return requests.get(_url('Function=OverlayInput2Out&Input=MatchResult'))


# Match Preview
def set_red1_preview(text, _url):
    return requests.get(_url('Function=SetText&Input=MatchPreview&SelectedName=Red1.Text&Value={:s}'.format(text)))
def set_red2_preview(text, _url):
    return requests.get(_url('Function=SetText&Input=MatchPreview&SelectedName=Red2.Text&Value={:s}'.format(text)))
def set_blue1_preview(text, _url):
    return requests.get(_url('Function=SetText&Input=MatchPreview&SelectedName=Blue1.Text&Value={:s}'.format(text)))
def set_blue2_preview(text, _url):
    return requests.get(_url('Function=SetText&Input=MatchPreview&SelectedName=Blue2.Text&Value={:s}'.format(text)))

# Match Result
def set_red1_result(text, _url):
    return requests.get(_url('Function=SetText&Input=MatchResult&SelectedName=Red1.Text&Value={:s}'.format(text)))
def set_red2_result(text, _url):
    return requests.get(_url('Function=SetText&Input=MatchResult&SelectedName=Red2.Text&Value={:s}'.format(text)))
def set_blue1_result(text, _url):
    return requests.get(_url('Function=SetText&Input=MatchResult&SelectedName=Blue1.Text&Value={:s}'.format(text)))
def set_blue2_result(text, _url):
    return requests.get(_url('Function=SetText&Input=MatchResult&SelectedName=Blue2.Text&Value={:s}'.format(text)))
def set_red_final_score(text, _url):
    return requests.get(_url('Function=SetText&Input=MatchResult&SelectedName=RedScore.Text&Value={:s}'.format(text)))
def set_blue_final_score(text, _url):
    return requests.get(_url('Function=SetText&Input=MatchResult&SelectedName=BlueScore.Text&Value={:s}'.format(text)))