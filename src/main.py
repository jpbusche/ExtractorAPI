from ext.currency import Currency
from ext.steam_api import SteamAPI
from ext.steam_spy import SteamSpy
from ext.youtube_api import YoutubeAPI
from ext.extractor import GameNotFound, PageNotFound
from db.elastic import Elastic
from utils import setup_logger, get_all_games

steam_api = SteamAPI()
steam_spy = SteamSpy()
steam_currency = Currency()
youtube_api = YoutubeAPI()

log = setup_logger()
log.info('Initializing Elasticsearch')
try:
	elastic = Elastic('elastic:9200', 'steam')
	elastic.delete_index()
	log.info('Elasticsearch connected')
	games = get_all_games()
	for game in games:
		game_id, game_name = int(game[0]), str(game[1])
		log.info('Starting the extraction of game: %s - %s', game_id, game_name)
		try:
			game = steam_api.get_game(game_id)
			log.info('Steam API: successed!')
			game.update(steam_spy.get_game(game_id))
			log.info('Steam SPY: successed!')
			game.update(steam_currency.get_game(game_id))
			log.info('Steam Currency: successed!')
			game.update(youtube_api.get_game(game_name))
			log.info('Youtube API: successed!')
			log.info('Starting insersion in the Elasticsearch')
			elastic.update(game_id, game)
			log.info('Finishing insersion in the Elasticsearch')
		except Exception as error:
			log.error(error)
except Exception as error:
	log.error(error)
	