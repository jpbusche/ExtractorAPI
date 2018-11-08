from celery import Celery
from celery.schedules import crontab
from db.elastic import Elastic
from utils import get_all_games, setup_logger
from ext.currency import Currency
from ext.steam_api import SteamAPI
from ext.steam_spy import SteamSpy
from ext.youtube_api import YoutubeAPI
from ext.extractor import GameNotFound

app = Celery('schedule')
app.conf.broker_url = 'redis://redis:6379/0'
log = setup_logger()
fail_id = open("ids_fails.txt", "a")
elastic = Elastic('elastic:9200', 'steam')

@app.task
def insert_new_games():
	lst1 = elastic.get_all()
	lst2 = get_all_games()
	print(lst2)
	# print(games)

@app.task
def update_steam_api():
	steam_api = SteamAPI()
	games = elastic.get_all()
	for game in games:
		log.info('Starting the extraction of game: %s - %s', game[0], game[1])
		try:
			gm = steam_api.get_game(int(game[0]))
			log.info('Extraction successed!')
			log.info('Starting update in the Elasticsearch')
			elastic.update(int(game[0]), gm)
			log.info('Finishing update in the Elasticsearch')
		except Exception as error:
			if type(error) == GameNotFound:
				log.warning(error)
			else:
				log.error(error)
			fail_id.write(str(game[0]) + " " + str(game[1]) + "\n")

@app.task
def update_steam_spy():
	steam_spy = SteamSpy()
	games = elastic.get_all()
	for game in games:
		log.info('Starting the extraction of game: %s - %s', game[0], game[1])
		try:
			gm = steam_spy.get_game(int(game[0]))
			log.info('Extraction successed!')
			log.info('Starting update in the Elasticsearch')
			elastic.update(int(game[0]), gm)
			log.info('Finishing update in the Elasticsearch')
		except Exception as error:
			if type(error) == GameNotFound:
				log.warning(error)
			else:
				log.error(error)
			fail_id.write(str(game[0]) + " " + str(game[1]) + "\n")

@app.task
def update_steam_currency():
	currency = Currency()
	games = elastic.get_all()
	for game in games:
		log.info('Starting the extraction of game: %s - %s', game[0], game[1])
		try:
			gm = currency.get_game(int(game[0]))
			log.info('Extraction successed!')
			log.info('Starting update in the Elasticsearch')
			elastic.update(int(game[0]), gm)
			log.info('Finishing update in the Elasticsearch')
		except Exception as error:
			if type(error) == GameNotFound:
				log.warning(error)
			else:
				log.error(error)
			fail_id.write(str(game[0]) + " " + str(game[1]) + "\n")

@app.task
def update_youtube_api():
	youtube_api = YoutubeAPI()
	games = elastic.get_all()
	for game in games:
		log.info('Starting the extraction of game: %s - %s', game[0], game[1])
		try:
			gm = youtube_api.get_game(str(game[1]))
			log.info('Extraction successed!')
			log.info('Starting update in the Elasticsearch')
			elastic.update(int(game[0]), gm)
			log.info('Finishing update in the Elasticsearch')
		except Exception as error:
			if type(error) == GameNotFound:
				log.warning(error)
			else:
				log.error(error)
			fail_id.write(str(game[0]) + " " + str(game[1]) + "\n")

update_steam_currency()

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
# 	log.info('Updating data from Steam API!')
# 	sender.add_periodic_task(6000.0, update_steam_api())