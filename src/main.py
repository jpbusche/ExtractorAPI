from ext.currency import Currency
from ext.steam_api import SteamAPI
from ext.steam_spy import SteamSpy
from ext.youtube_api import YoutubeAPI
from ext.extractor import GameNotFound
from db.elastic import Elastic
from utils import setup_logger, get_all_games
import time

steam_api = SteamAPI()
steam_spy = SteamSpy()
steam_currency = Currency()
youtube_api = YoutubeAPI()

log = setup_logger()
log.info('Initializing Elasticsearch')
fail_id = open("ids_fails.txt", "a")

index_body = {
	"mapping": {
		"game": {
			"properties": {
				"name": { "type": "keyword" },
				"description": { "type": "keyword" },
				"header_image": { "type": "keyword" },
				"background_image": { "type": "keyword" },
				"website": { "type": "keyword" },
				"release_date": { "type": "nested",
					"properties": {
						"release_month": { "type": "keyword" },
						"release_year": { "type": "long" },
						"release_day": { "type": "long" },		
					}},
				"steam_id": { "type": "long" },
				"metacritic_score": { "type": "long" },
				"positive_avaliantion": { "type": "long" },
				"negative_avaliantion": { "type": "long" },
				"genres": { "type": "keyword", "store": "true" },
				"categories": { "type": "keyword", "store": "true" },
				"languages": { "type": "keyword", "store": "true" },
				"screenshots": { "type": "keyword", "store": "true" },
				"developers": { "type": "keyword", "store": "true" },
				"publishers": { "type": "keyword", "store": "true" },
				"platforms": { "type": "keyword", "store": "true" },
			}
		},
	}
}

try:
	elastic = Elastic('elastic:9200', 'steam_est')
	log.info('Elasticsearch connected')
	log.info('Creating index Steam Estastic on Elasticsearch')
	elastic.create_index(index_body)
	log.info('Index Steam Created')
	games = get_all_games()
	log.debug(len(games))
	for game in games:
		game_id, game_name = int(game[0]), str(game[1])
		log.info('Starting the extraction of game: %s - %s', game_id, game_name)
		try:
			game = steam_api.get_game(game_id, 'estastic')
			log.info('Steam API: successed!')
			game.update(steam_spy.get_game(game_id, 'estastic'))
			log.info('Steam SPY: successed!')
			log.info('Starting insersion in the Elasticsearch')
			elastic.update(game_id, game, 'game_est')
			log.info('Finishing insersion in the Elasticsearch')
		except Exception as error:
			if type(error) == GameNotFound:
				log.warning(error)
			else:
				log.error(error)
			time.sleep(300)
			fail_id.write(str(game_id) + " || " + str(game_name) + "\n")
except Exception as error:
	log.error(error)

log.info('First insersion completed')