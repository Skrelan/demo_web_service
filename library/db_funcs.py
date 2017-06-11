import web
import config.configs as configs
import logging
import misc
import requests
import time

logging.basicConfig( 
	level=logging.DEBUG,
	format="[%(asctime)s] | [%(levelname)s] | %(message)s")

C = configs.Configs()

def query_db(query):
	"""
	About:
		This function is used to query the Postgress db
	
		Args: query (str)
		Returns: list or False
	"""
	try:
		db = web.database(dbn='postgres', 
						  db='postgres', 
						  user='postgres', 
						  pw=C.secrets["postgres"])

		results = db.query(query)
		return results

	except Exception as e:
		logging.error("database connection failed\n{0}\nAborting".format(e))
		return False


def batch_query_db(data):
	print "in"
	batch_size = C.database_batch_size
	batch = []
	for i,val in enumerate(data):
		batch.append(val)
		if i%batch_size == 0 and i>0:
			logging.info("Data batch-{0} :{1}".format(i/batch_size,batch))
			logging.info("start: {0} -> end {1}".format(i-batch_size,i))
			batch = []
	if len(batch) > 0:
		logging.info("Data batch-{0} :{1}".format((i/batch_size)+1,batch))
		logging.info(len(batch))


@misc.time_taken
def write_response_to_file(file_name,url):
	"""
	About:
		This function is used to added the response to a file

		Args: file_name (str), url (str)
		Returns: Bool
	"""
	try:
		r = requests.get(url,stream=True)
		path = 'json_data/{0}'
		try:
			with open(path.format(file_name), 'wb') as fd:
				i = 0
				for chunk in r.iter_content(chunk_size=128):
					i +=1
					fd.write(chunk)
					if i%128==0:
						logging.info('chunk: {} completed'.format(i))
			return True

		except Exception as e:
			logging.error("File handling error: {}".format(e)) 
			return False

	except Exception as e:
		logging.error(misc.generate_error('Invalid Advertiser, {0}'.format(
			data.advertiser)))
		logging.error('Exception caught: {}'.format(e))


def add_vendor(data):
	"""
	About:
		This function is used to add a data to products table in the Postgres db

		Args: data (object of web.utils.Storage)
		Returns: Bool
	"""
	url = C.urls['vendor'].format(data.advertiser,C.secrets['admin_token'])
	file_name = data.advertiser+'_products.json'
	
	file_created = write_response_to_file(file_name,url)

	if file_created:
		resp = misc.generate_success("File added")
	else:
		resp = misc.generate_error("File failed to be created")


	return resp
