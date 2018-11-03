import colorlog
import requests
import json

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