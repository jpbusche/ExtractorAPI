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
				"name": { "type": "keyword" },
				"description": { "type": "keyword" },
				"header_image": { "type": "keyword" },
				"background_image": { "type": "keyword" },
				"website": { "type": "keyword" },
				"release_date": { "type": "keyword" },
				"steam_id": { "type": "long" },
				"metacritic_score": { "type": "long" },
				"positive_avaliantion": { "type": "long" },
				"negative_avaliantion": { "type": "long" },
				"median_hours_played": { "type": "nested",
					"properties": {
						"value": { "type": "double" },
						"date": {"type": "date"}
					} },
				"owners": { "type": "nested",
					"properties": {
						"value": { "type": "double" },
						"date": {"type": "date"}
					} },
				"currency": { "type": "nested",
					"properties": {
						"value": { "type": "double" },
						"date": {"type": "date"}
					} },
				"view_count": { "type": "nested",
					"properties": {
						"value": { "type": "double" },
						"date": {"type": "date"}
					} },
				"like_count": { "type": "nested",
					"properties": {
						"value": { "type": "double" },
						"date": {"type": "date"}
					} },
				"dislike_count": { "type": "nested",
					"properties": {
						"value": { "type": "double" },
						"date": {"type": "date"}
					} },
				"userscore": { "type": "nested",
					"properties": {
						"value": { "type": "double" },
						"date": {"type": "date"}
					} },
				"genres": { "type": "keyword", "store": "true" },
				"categories": { "type": "keyword", "store": "true" },
				"languages": { "type": "keyword", "store": "true" },
				"screenshots": { "type": "keyword", "store": "true" },
				"developers": { "type": "keyword", "store": "true" },
				"publishers": { "type": "keyword", "store": "true" },
				"platforms": { "type": "keyword", "store": "true" },
				"is_free": { "type": "boolean" },
				"price": { "type": "nested",
					"properties": {
						"value": { "type": "double" },
						"date": {"type": "date"}
					}}
			}
		}
	}
}

try:
	elastic = Elastic('elastic:9200', 'steam')
	log.info('Elasticsearch connected')
	log.info('Creating index Steam on Elasticsearch')
	elastic.create_index(index_body)
	log.info('Index Steam Created')
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

log.info('First insersion completed')