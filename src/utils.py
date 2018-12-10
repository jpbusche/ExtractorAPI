import colorlog
import requests
import json
from ext.extractor import PageNotFound

def setup_logger():
	formatter = colorlog.ColoredFormatter(
		"%(asctime)s -- %(log_color)s %(levelname)s: %(message)s",
		datefmt = '%d/%m/%y|%H:%M:%S',
		reset = True,
		log_colors = {
			'DEBUG': 'cyan',
			'INFO': 'green',
			'WARNING': 'purple',
			'ERROR': 'red',
			'CRITICAL': 'bold_red'
		}
	)
	handler = colorlog.StreamHandler()
	handler.setFormatter(formatter)
	logger = colorlog.getLogger('Extractor')
	logger.addHandler(handler)
	logger.setLevel('DEBUG')
	return logger

def get_all_games():
	games = []
	response = requests.get('http://steamspy.com/api.php?request=all')
	if response.status_code == requests.codes.ok:
		response = json.loads(response.content)
		for game in response:
			pair = (response[game]['appid'], response[game]['name'])
			games.append(pair)
		return games
	else:
		raise PageNotFound("Page not found!!!")

def get_games_db():
	games = []
	response = requests.get('http://elastic:9200/steam_est/_search?')
	response = json.loads(response.content)
	total = response['hits']['total']
	response = requests.get('http://elastic:9200/steam_est/_search?size=' + str(total))
	response = json.loads(response.content)['hits']['hits']
	for game in response:
		pair = (game['_source']['steam_id'], game['_source']['name'])
		games.append(pair)
	return games