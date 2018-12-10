from celery import Celery
from celery.schedules import crontab
from db.elastic import Elastic
from utils import get_all_games, setup_logger, get_games_db
from ext.currency import Currency
from ext.steam_api import SteamAPI
from ext.steam_spy import SteamSpy
from ext.youtube_api import YoutubeAPI
from ext.extractor import GameNotFound
import os
import time

app = Celery('schedule')
steam_api = SteamAPI()
steam_spy = SteamSpy()
steam_currency = Currency()
youtube_api = YoutubeAPI()
app.conf.broker_url = 'redis://redis:6379/0'
log = setup_logger()
up_games = get_games_db()

@app.task
def insert_new_games():
	elastic = Elastic('elastic:9200', 'steam_est')
	log.info('Insert new games on Elasticsearch!')
	fail_id = open("ids_fails.txt", "a")
	lst1 = elastic.get_all()
	lst2 = get_all_games()
	games = [game for game in lst2 if game not in lst1]
	for game in games:
		game_id, game_name = int(game[0]), str(game[1])
		log.info('Starting the extraction of game: %s - %s', game_id, game_name)
		try:
			game = steam_api.get_game(game_id, 'estastic')
			log.info('Steam API: successed!')
			game.update(steam_spy.get_game(game_id, 'estastic'))
			log.info('Steam SPY: successed!')
			game.update(steam_currency.get_game(game_id, 'estastic'))
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

@app.task
def update_steam_api():
	elastic = Elastic('elastic:9200', 'steam_tmp')
	log.info('Updating data from Steam API!')
	for game in up_games:
		log.info('Starting the extraction of game: %s - %s', game[0], game[1])
		try:
			gm = steam_api.get_game(int(game[0]), 'temporal')
			log.info('Extraction successed!')
			log.info('Starting update in the Elasticsearch')
			elastic.update(int(game[0]), gm, 'game_tmp')
			log.info('Finishing update in the Elasticsearch')
		except Exception as error:
			if type(error) == GameNotFound:
				log.warning(error)
			else:
				log.error(error)
			time.sleep(300)
			games.append(game)

@app.task
def update_steam_spy():
	elastic = Elastic('elastic:9200', 'steam_tmp')
	log.info('Updating data from Steamspy API!')
	for game in up_games:
		log.info('Starting the extraction of game: %s - %s', game[0], game[1])
		try:
			gm = steam_spy.get_game(int(game[0]), 'temporal')
			log.info('Extraction successed!')
			log.info('Starting update in the Elasticsearch')
			elastic.update(int(game[0]), gm, 'game_tmp')
			log.info('Finishing update in the Elasticsearch')
		except Exception as error:
			if type(error) == GameNotFound:
				log.warning(error)
			else:
				log.error(error)
			games.append(game)

@app.task
def update_steam_currency():
	elastic = Elastic('elastic:9200', 'steam_tmp')
	log.info('Updating data from Steam Currency!')
	for game in up_games:
		log.info('Starting the extraction of game: %s - %s', game[0], game[1])
		try:
			gm = steam_currency.get_game(int(game[0]), 'temporal')
			log.info('Extraction successed!')
			log.info('Starting update in the Elasticsearch')
			elastic.update(int(game[0]), gm, 'game_tmp')
			log.info('Finishing update in the Elasticsearch')
		except Exception as error:
			if type(error) == GameNotFound:
				log.warning(error)
			else:
				log.error(error)
			time.sleep(300)
			games.append(game)

@app.task
def update_youtube_api():
	elastic = Elastic('elastic:9200', 'steam_tmp')
	log.info('Updating data from Youtube API!')
	for game in up_games:
		log.info('Starting the extraction of game: %s - %s', game[0], game[1])
		try:
			gm = youtube_api.get_game(str(game[1]), 'temporal')
			log.info('Extraction successed!')
			log.info('Starting update in the Elasticsearch')
			elastic.update(int(game[0]), gm, 'game_tmp')
			log.info('Finishing update in the Elasticsearch')
		except Exception as error:
			if type(error) == GameNotFound:
				log.warning(error)
			else:
				log.error(error)
		time.sleep(3600)
		games.append(game)


@app.task
def try_fails_id():
	elastic = Elastic('elastic:9200', 'steam_est')
	log.info('Trying insert the fails ids again!')
	games = open("ids_fails.txt", "r")
	for game in games:
		game_id, game_name = game.split(" || ")
		game_id = int(game_id)
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
	os.remove("ids_fails.txt")

app.conf.beat_schedule = {
	"update-steam-api": {
		"task": "schedule.update_steam_api",
		"schedule": crontab(minute=0, hour=0)
	},
	"update-steamspy-api": {
		"task": "schedule.update_steam_spy",
		"schedule": crontab(minute=0, hour=0)
	},
	"update-currency-api": {
		"task": "schedule.update_steam_currency",
		"schedule": crontab(minute=0, hour=0)
	},
	"update-youtube-api": {
		"task": "schedule.update_youtube_api",
		"schedule": crontab(minute=0, hour=0)
	},
	"insert-new-games": {
		"task": "schedule.insert_new_games",
		"schedule": crontab(minute=0, hour=0, day_of_week='sunday')
	},
	"try-fails-id": {
		"task": "schedule.try_fails_id",
		"schedule": crontab(minute=0, hour=0, day_of_week='saturday')
	}
}