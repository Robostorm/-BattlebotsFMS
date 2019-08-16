import vmix

ipaddr = '127.0.0.1'
def _url(path):
    return 'http://' + ipaddr + ':8088/api/?' + path

resp = vmix.set_red_score(15, _url)
resp = vmix.set_blue_score(30, _url)
resp = vmix.set_game_clock('00:02:00', _url)
resp = vmix.stop_game_clock(_url)
resp = vmix.start_game_clock(_url)
resp = vmix.set_scoreboard_top_text('Robostorm Battlebots 2019', _url)
resp = vmix.overlay_match_preview_in(_url)
resp = vmix.overlay_scoreboard_in(_url)