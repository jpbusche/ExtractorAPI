from ext.extractor import Extractor, GameNotFound

class SteamAPI(Extractor):

	url = 'https://store.steampowered.com/api/appdetails/?appids={}&cc=pt-br'

	def get_game(self, identifier, flag):
		response = self.get_api(identifier)
		data = response[str(identifier)]
		if data['success'] and data is not None:
			if flag == 'estastic':
				result = self.manipulate_data_est(data['data'])
				return result
			elif flag == 'temporal':
				result = self.manipulate_data_tmp(data['data'], identifier)
				return result
			else:
				raise DataTypeNotFound('Data type not found!!!')
		else:
			raise GameNotFound("Game not found!!!")

	def manipulate_data_est(self, data):
		result = {}
		result['genres'] = []
		result['publishers'] = []
		result['developers'] = []
		result['platforms'] = []
		result['screenshots'] = []
		result['name'] = data['name']
		result['steam_id'] = data['steam_appid']
		result['description'] = data['about_the_game']
		result['header_image'] = data['header_image']
		result['background_image'] = data['background']
		if data['website'] is not None:
			result['website'] = data['website']
		else:
			result['website'] = ""
		if 'genres' in data:
			for gnr in data['genres']:
				result['genres'].append(gnr['description'])
		for pbl in data['publishers']:
			result['publishers'].append(pbl)
		if 'developers' in data:
			for dvp in data['developers']:
				result['developers'].append(dvp)
		for plt in data['platforms']:
			if plt: result['platforms'].append(str(plt).capitalize())
		if data['release_date']['date'] != "":
			result['release_date'] = data['release_date']['date']
		else:
			result['release_date'] = '12 Set, 2003'
		if 'metacritic' in data:
			result['metacritic_score'] = data['metacritic']['score']
		else:
			result['metacritic_score'] = 0
		for screen in data['screenshots']:
			result['screenshots'].append(screen['path_full'])
		return result

	def manipulate_data_tmp(self, data, identifier):
		result = {}
		if data['is_free'] or not 'price_overview' in data:
			result['price'] = self.temporal_data(identifier, 0.0, 'price')
			result['is_free'] = True
		else:
			result['price'] = self.temporal_data(identifier, data['price_overview']['final'] / 100, 'price')
			result['is_free'] = False
		return result