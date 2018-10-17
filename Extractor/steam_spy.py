import requests
import json
from extractor import Extractor

class SteamSpy(Extractor):
	
	def get_game(self, identifier):
		url = 'http://steamspy.com/api.php?request=appdetails&appid=' + str(identifier)
		response = requests.get(url)
		if response.status_code == requests.codes.ok:
			data = json.loads(response.text)
			if data['name'] is not None:
				result = {}
				result['languages'] = []
				result['categories'] = []
				for lng in data['languages'].split(', '):
					result['languages'].append(lng)
				total = data['positive'] + data['negative']
				rating = (float(data['positive']) / float(total)) * 100
				result['rating'] = round(rating, 2)
				for ctg in data['tags']:
					result['categories'].append(ctg)
				num = data['owners'].split(' .. ')
				ow1 = int(num[0].replace(",", ""))
				result['owners'] = int((int(num[0].replace(",", "")) + int(num[1].replace(",", ""))) / 2)
				return json.dumps(result)
			else:
				raise Exception("Jogo não encontrado!!!") 
		else:
			raise Exception("Página não encontrada!!!")