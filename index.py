import web
import logging
import json
import config.configs as configs
import os
import requests
import urlparse
import library.db_funcs as db_funcs
import library.misc as misc

logging.basicConfig( 
	level=logging.DEBUG,
	format="[%(asctime)s] | [%(levelname)s] | %(message)s")

logging.info("#"*20)
logging.info("Starting the app")

urls = ('/','Index',
		'/test','Test',
		'/apiTester','Api_tester',
		'/addVendor','Add_vendor',
		'/search','Search',
		'/products','Products')

app = web.application(urls, globals())
web.config.debug = True

C = configs.Configs()

"""
Let's keep all the configs above this, for our ease.
"""


class Index:
	'''
	About: 
		This handles the landing page section of this app.
	'''
	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self,name=''):
		query = "Select * from users"
		results = db_funcs.query_db(query)

		if results:
			return self.render.index("hello is cool",results)
		else:
			logging.error('Invalid Query {0}'.format(query))
			return self.render.index("Something broke",[])


class Test:
	"""
	About: 
		This is a test endpoint that we can ping to verify 
		if the app is running.
	"""
	def GET(self,name=''):
		return json.dumps({'message':'yes, I work','version':'1.0'})

	def POST(self):
		data = json.loads(web.data())
		logging.info(data)
		return json.dumps(data)


class Api_tester:
	"""
	About:
		This hosts the /apiTester page from where we can explore
		the API's.
		
		GET req: hosts the page
		POST req: executes the requests
	"""
	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self):
		return self.render.testpage()

	def POST(self):
		data = json.loads(web.data())
		if data['req'] == 'POST':
			url = data['url']
			parsed = urlparse.urlparse(url)
			outgoing = urlparse.parse_qs(parsed.query)
			r = requests.post(url,json.dumps(outgoing))
		else:
			url = data['url']
			parsed = urlparse.urlparse(url)
			outgoing = urlparse.parse_qs(parsed.query)
			r = requests.get(url,json.dumps(outgoing))
		logging.info(r)
		logging.info("the response sent back is as below:")
		logging.debug(r.content)
		return r.content


class Add_vendor:
	"""
	About:
		This adds the products of a vendor into the database,
		if the vendor does not already exsist in the database.
	"""
	def GET(self):
		data = web.input(advertiser=None)
		
		'''
		parsed = urlparse.urlparse(web.ctx.query)
		outgoing = urlparse.parse_qs(parsed.query)
		'''
		
		if not data.advertiser:
			return misc.generate_error("'advertiser' field expected")

		else:
			r = requests.get(C.urls['vendor'].format(data.advertiser,C.secrets['admin_token']))
			try:
				resp = r.json()
				db_funcs.batch_query_db(resp['products'])
			except:
				resp = misc.generate_error('Invalid Advertiser, {0}'.format(
					data.advertiser))
			return resp


if __name__ == '__main__':
		app.run()
