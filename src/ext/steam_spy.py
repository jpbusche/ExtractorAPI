from ext.extractor import Extractor, GameNotFound

class SteamSpy(Extractor):
	
	url = 'http://steamspy.com/api.php?request=appdetails&appid={}'

	def get_game(self, identifier):
		response = self.get_api(identifier)
		if response['name'] is not None:
			result = self.manipulate_data(response, identifier)
			return result
		else:
			raise GameNotFound("Game not found!!!")

	def manipulate_data(self, data, identifier):
		result = {}
		result['languages'] = []
		result['categories'] = []
		result['positive_avaliantion'] = data['positive']
		result['negative_avaliantion'] = data['negative']
		total = data['positive'] + data['negative']
		score = data['positive'] / total * 100
		result['userscore'] = self.temporal_data(identifier, round(score, 2), 'userscore')
		result['median_hours_played'] = self.temporal_data(identifier, data['median_forever'] // 60, 'median_hours_played')
		numbers = data['owners'].split(' .. ')
		own = (int(numbers[0].replace(',', '')) + int(numbers[1].replace(',', ''))) // 2
		result['owners'] = self.temporal_data(identifier, own, 'owners')
		for lng in data['languages'].split(', '):
			result['languages'].append(lng)
		for ctg in data['tags']:
			result['categories'].append(ctg)
		return result