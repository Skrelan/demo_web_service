import web
import logging
import json
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


class Index:
	'''
	About: 
		This handles the landing page section of this app.
	'''
	def __init__(self):
		self.render = web.template.render('templates/')

	def GET(self,name=''):
		return self.render.index("Products List")

	def POST(self):
		return misc.generate_error("Invalid request")


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
		return misc.generate_error("Invalid request")

	def POST(self):
		data = web.input(advertiser=None)

		if not data.advertiser:
			return misc.generate_error("'advertiser' field expected")

		else:
			resp = db_funcs.add_vendor(data)
			return resp

class Search:
	"""
	About:
		This enables users and scripts to Search the Database,
		using URL pased search queries
	"""
	def GET(self):
		try:
			data = json.loads(web.data())
			data = misc.convert_to_namedtuple(
						{'advertiser':None,
						 'designer':None,
						 'keywords':None,
						 'min_price':None,
						 'max_price':None,
						 'limit':None,
						 'offset':None},data)
		except:
			data = web.input(advertiser=None,
						 designer=None,
						 keywords=None,
						 min_price=None,
						 max_price=None,
						 limit=None,
						 offset=None)

		resp = db_funcs.search_product(data)
		return resp

	def POST(self):
		return misc.generate_error('Invalid request. Nice try ;)')

class Products:
	"""
	About:
		This is used by landing page to load data
	""" 
	def GET(self):
		resp = db_funcs.load_product()
		return resp

	def POST(self):
		resp = db_funcs.load_product()
		return resp


if __name__ == '__main__':
		app.run()
