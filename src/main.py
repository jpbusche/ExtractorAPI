from ext.currency import Currency
from ext.steam_api import SteamAPI
from ext.steam_spy import SteamSpy
from ext.youtube_api import YoutubeAPI
from ext.extractor import GameNotFound
from db.elastic import Elastic
from utils import setup_logger, get_all_games

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
				"name": { "type": "text" },
				"description": { "type": "text" },
				"header_image": { "type": "text" },
				"background_image": { "type": "text" },
				"website": { "type": "text" },
				"release_date": { "type": "text" },
				"steam_id": { "type": "long" },
				"metacritic_score": { "type": "long" },
				"positive_avaliantion": { "type": "long" },
				"negative_avaliantion": { "type": "long" },
				"median_hours_played": { "type": "long" },
				"owners": { "type": "long" },
				"currency": { "type": "long" },
				"view_count": { "type": "long" },
				"like_count": { "type": "long" },
				"dislike_count": { "type": "long" },
				"userscore": { "type": "double" },
				"genres": { "type": "text", "store": "true" },
				"categories": { "type": "text", "store": "true" },
				"languages": { "type": "text", "store": "true" },
				"screenshots": { "type": "text", "store": "true" },
				"developers": { "type": "text", "store": "true" },
				"publishers": { "type": "text", "store": "true" },
				"platforms": { "type": "text", "store": "true" },
				"is_free": {"type": "boolean"},
				"price": {
					"type": "nested",
					"properties": {
						"value": { "type": "double" },
						"date": {"type": "date"}
					}
				}
			}
		}
	}
}

try:
	elastic = Elastic('elastic:9200', 'steam')
	log.info('Elasticsearch connected')
	log.info('Create index Steam on Elasticsearch')
	elastic.create_index(index_body)
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
			if type(error) == GameNotFound:
				log.warning(error)
			else:
				log.error(error)
				fail_id.write(str(game_id) + " || " + str(game_name) + "\n")
except Exception as error:
	log.error(error)