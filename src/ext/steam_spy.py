from ext.extractor import Extractor, GameNotFound

class SteamSpy(Extractor):
	
	url = 'http://steamspy.com/api.php?request=appdetails&appid={}'

	def get_game(self, identifier):
		response = self.get_api(identifier)
		if response['name'] is not None:
			result = self.manipulate_data(response)
			return result
		else:
			raise GameNotFound("Jogo não encontrado!!!")

	def manipulate_data(self, data):
		result = {}
		result['languages'] = []
		result['categories'] = []
		result['positive_avaliantion'] = data['positive']
		result['negative_avaliantion'] = data['negative']
		total = data['positive'] + data['negative']
		score = data['positive'] / total * 100
		result['userscore'] = round(score, 2)
		result['median_hours_played'] = data['median_forever'] // 60
		numbers = data['owners'].split(' .. ')
		result['owners'] = (int(numbers[0].replace(',', '')) + int(numbers[1].replace(',', ''))) // 2
		for lng in data['languages'].split(', '):
			result['languages'].append(lng)
		for ctg in data['tags']:
			result['categories'].append(ctg)
		return result