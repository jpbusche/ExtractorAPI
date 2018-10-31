from ext.extractor import Extractor, GameNotFound

class SteamAPI(Extractor):

	url = 'https://store.steampowered.com/api/appdetails/?appids={}'

	def get_game(self, identifier):
		response = self.get_api(identifier)
		data = response[str(identifier)]
		if data['success'] and data is not None:
			result = self.manipulate_data(data['data'])
			return result
		else:
			raise GameNotFound("Game not found!!!")

	def manipulate_data(self, data):
		result = {}
		result['genres'] = []
		result['publishers'] = []
		result['developers'] = []
		result['platforms'] = []
		result['screenshots'] = []
		result['name'] = data['name']
		result['steam_id'] = data['steam_appid']
		if data['is_free'] or data['price_overview'] is None:
			result['price'] = 0.0
			result['is_free'] = True
		else:
			result['price'] = data['price_overview']['initial'] / 100
			result['is_free'] = False
		result['description'] = data['about_the_game']
		result['header_image'] = data['header_image']
		result['background_image'] = data['background']
		if data['website'] is not None:
			result['website'] = data['website']
		else:
			result['website'] = ""
		for gnr in data['genres']:
			result['genres'].append(gnr['description'])
		for pbl in data['publishers']:
			result['publishers'].append(pbl)
		for dvp in data['developers']:
			result['developers'].append(dvp)
		for plt in data['platforms']:
			if plt: result['platforms'].append(str(plt).capitalize())
		if data['release_date']['date'] != "":
			result['date'] = data['release_date']['date']
		else:
			result['date'] = '12 Set, 2003'
		if 'metacritic' in data:
			result['metacritic_score'] = data['metacritic']['score']
		else:
			result['metacritic_score'] = 0
		for screen in data['screenshots']:
			result['screenshots'].append(screen['path_full'])
		return result