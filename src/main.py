from ext.currency import Currency
from ext.steam_api import SteamAPI
from ext.steam_spy import SteamSpy
from db.elastic import Elastic

elastic = Elastic('elastic:9200', 'test')
id = input("Entre com o número de ID: ")
stapi = SteamAPI()
stspy = SteamSpy()
curr = Currency()
game = stapi.get_game(id)
game.update(stspy.get_game(id))
game.update(curr.get_game(id))
elastic.update(id, game)