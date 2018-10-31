from ext.currency import Currency
from ext.steam_api import SteamAPI
from ext.steam_spy import SteamSpy
from ext.youtube_api import YoutubeAPI
from ext.extractor import GameNotFound, PageNotFound
from db.elastic import Elastic
import colorlog

stapi = SteamAPI()
stspy = SteamSpy()
curr = Currency()
youapi = YoutubeAPI()

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

id = input("Entre com o número de ID: ")
log = setup_logger()
log.info('Initializing Elasticsearch')
try:
	elastic = Elastic('elastic:9200', 'test')
	log.info('Elasticsearch connected')
	log.info('Starting the extraction of id: %s', str(id))
	game = stapi.get_game(id)
	log.info('Steam API: successed!')
	game.update(stspy.get_game(id))
	log.info('Steam SPY: successed!')
	game.update(curr.get_game(id))
	log.info('Steam Currency: successed!')
	if 'name' in game:
		game.update(youapi.get_game(game['name']))
		log.info('Youtube API: successed!')
	else: raise GameNotFound('Game not found!!!')
	log.info('Starting insersion in the Elasticsearch')
	elastic.update(id, game)
	log.info('Finishing insersion in the Elasticsearch')
	elastic.delete(id)
except GameNotFound as error:
	log.warning(error)	
except PageNotFound as error:
	log.error(error)
except Exception as error:
	log.error(error)
	