import web
import logging
import json
import config.configs as configs
import os

logging.basicConfig( 
	level=logging.DEBUG,
	format="[%(asctime)s] | [%(levelname)s] | %(message)s")

urls = ('/','Index',
		'/test','Test')

app = web.application(urls, globals())
web.config.debug = True

C = configs.Configs()

try:
	db = web.database(dbn='postgres', db='postgres', user='postgres', pw=C.logins["postgres"])
	is_db_connected = True
except Exception as e:
	logging.error("database connection failed\n{0}\nAborting".format(e))
	is_db_connected = False

class Index:
	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self,name=''):
		payload = {'name':name,'message':'Hello World'}
		logging.info(payload)
		t = range(0,10)
		results = db.query("Select * from users")
		return self.render.index("hello is cool",results)

	def POST(self):
		data = json.loads(web.data())
		logging.info(data)
		return 'found shit/n'


class Test:
	def GET(self,name=''):
		return json.dumps({'message':'yes, I work'})

	def POST(self):
		data = json.loads(web.data())
		logging.info(data)
		return data

if __name__ == '__main__':
	#if is_db_connected:
	port = int(os.environ.get('PORT', 8080))
	app.run()
