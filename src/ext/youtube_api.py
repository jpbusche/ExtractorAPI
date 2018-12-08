from ext.extractor import Extractor, GameNotFound, PageNotFound
import requests
import json

class YoutubeAPI(Extractor):

	API_KEY = 'AIzaSyD7uEK8S8NE79iHUx70rTvwXBCEHp5BosQ'

	def get_game(self, identifier, flag):
		videos = self.get_videos(identifier)
		if len(videos) != 0:
			result = {}
			if flag == 'estastic':
				return result
			elif flag == 'temporal':
				result = self.manipulate_data_tmp(videos, identifier)
				return result
			else:
				raise DataTypeNotFound('Data type not found!!!')
		else:
			raise GameNotFound("Game not found!!!")


	def get_videos(self, identifier):	
		videos_id = []
		url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q={}&type=video&key={}&order=relevance'
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

	def manipulate_data_tmp(self, data, identifier):
		result = {}
		url = 'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={}&key={}'
		sum_view = 0
		sum_like = 0
		sum_dislike = 0
		for vid in data:
			response = self.get_api(url, vid)['items'][0]['statistics']
			if 'viewCount' in response: sum_view += int(response['viewCount'])
			if 'likeCount' in response: sum_like += int(response['likeCount'])
			if 'dislikeCount' in response: sum_dislike += int(response['dislikeCount'])
		result['view_count'] = self.temporal_data(identifier, sum_view, 'view_count')
		result['like_count'] = self.temporal_data(identifier, sum_like, 'like_count')
		result['dislike_count'] = self.temporal_data(identifier, sum_dislike, 'dislike_count')
		return result