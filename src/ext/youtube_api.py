from ext.extractor import Extractor, GameNotFound, PageNotFound
import requests
import json

class YoutubeAPI(Extractor):

	API_KEY = 'AIzaSyD7uEK8S8NE79iHUx70rTvwXBCEHp5BosQ'

	def get_game(self, identifier):
		videos = self.get_videos(identifier)
		if len(videos) != 0:
			result = self.manipulate_data(videos)
			return result
		else:
			raise GameNotFound("Game not found!!!")


	def get_videos(self, identifier):	
		videos_id = []
		url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=20&q={}&type=video&key={}&order=relevant'
		response = self.get_api(url, identifier)
		for vid in response['items']:
			videos_id.append(vid['id']['videoId'])
		return videos_id

	def get_api(self, url, identifier):
		response = requests.get(url.format(identifier, self.API_KEY))
		if response.status_code == requests.codes.ok:
			response = json.loads(response.text)
			return response
		else:
			raise PageNotFound("Page not found!!!")

	def manipulate_data(self, data):
		result = {'view_count': 0, 'like_count': 0, 'dislike_count': 0}
		url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={}&key={}'
		for vid in data:
			response = self.get_api(url, vid)['items'][0]['statistics']
			result['view_count'] += int(response['viewCount'])
			result['like_count'] += int(response['likeCount'])
			result['dislike_count'] += int(response['dislikeCount'])
			return result