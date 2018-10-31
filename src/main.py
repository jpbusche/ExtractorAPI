from ext.currency import Currency
from ext.steam_api import SteamAPI
from ext.steam_spy import SteamSpy
from db.elastic import Elastic
import colorlog

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

log = setup_logger()