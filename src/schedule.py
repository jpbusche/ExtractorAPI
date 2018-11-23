from celery import Celery
from celery.schedules import crontab
from db.elastic import Elastic
from utils import get_all_games, setup_logger
from ext.currency import Currency
from ext.steam_api import SteamAPI
from ext.steam_spy import SteamSpy
from ext.youtube_api import YoutubeAPI
from ext.extractor import GameNotFound
import os

app = Celery('schedule')
steam_api = SteamAPI()
steam_spy = SteamSpy()
steam_currency = Currency()
youtube_api = YoutubeAPI()
app.conf.broker_url = 'redis://redis:6379/0'
log = setup_logger()
elastic = Elastic('elastic:9200', 'steam')

@app.task
def insert_new_games():
	fail_id = open("ids_fails.txt", "a")
	lst1 = elastic.get_all()
	lst2 = get_all_games()
	games = [game for game in lst2 if game not in lst1]
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

@app.task
def update_steam_api():
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
			fail_id.write(str(game[0]) + " || " + str(game[1]) + "\n")

@app.task
def update_steam_spy():
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
			fail_id.write(str(game[0]) + " || " + str(game[1]) + "\n")

@app.task
def update_steam_currency():
	games = elastic.get_all()
	for game in games:
		log.info('Starting the extraction of game: %s - %s', game[0], game[1])
		try:
			gm = steam_currency.get_game(int(game[0]))
			log.info('Extraction successed!')
			log.info('Starting update in the Elasticsearch')
			elastic.update(int(game[0]), gm)
			log.info('Finishing update in the Elasticsearch')
		except Exception as error:
			if type(error) == GameNotFound:
				log.warning(error)
			else:
				log.error(error)
			fail_id.write(str(game[0]) + " || " + str(game[1]) + "\n")

@app.task
def update_youtube_api():
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
			fail_id.write(str(game[0]) + " || " + str(game[1]) + "\n")

@app.task
def try_fails_id():
	games = open("ids_fails.txt", "r")
	for game in games:
		game_id, game_name = game.split(" || ")
		game_id = int(game_id)
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
	os.remove("ids_fails.txt")

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
	log.info('Updating data from Steam API!')
	sender.add_periodic_task(crontab(minute=0, hour=0), update_steam_api())
	log.info('Updating data from Steamspy API!')
	sender.add_periodic_task(crontab(minute=0, hour=0), update_steam_spy())
	log.info('Updating data from Steam Currency!')
	sender.add_periodic_task(crontab(minute=0, hour=0), update_steam_currency())
	log.info('Updating data from Youtube API!')
	sender.add_periodic_task(crontab(minute=0, hour=0), update_youtube_api())
	log.info('Inserting new games!')
	sender.add_periodic_task(crontab(minute=0, hour=0, day_of_week='sunday'), insert_new_games())
	log.info('Trying again the fails inserts!')
	sender.add_periodic_task(crontab(minute=0, hour=0, day_of_week='sunday'), try_fails_id())