import web
import config.configs as configs
import logging
import misc
import requests
import time
import os
import json
from collections import defaultdict

logging.basicConfig( 
	level=logging.DEBUG,
	format="[%(asctime)s] | [%(levelname)s] | %(message)s")

C = configs.Configs()

json_dump_path = 'json_data/{0}'
no_key_response = '<Code>NoSuchKey</Code>'

list_of_items = ['products.item.product_id','products.item.product_name','products.item.product_url',
				 'products.item.advertiser','products.item.designer','products.item.image_url',
				 'products.item.price','products.item.commission']

alternate_list = ['products', ' ', None]

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
		try:
			with open(file_name, 'wb') as fd:
				i = 0
				for chunk in r.iter_content(chunk_size=128):
					
					if i == 0 and no_key_response in chunk:
						logging.error(misc.generate_error(
							'Invalid Advertiser'))
						break

					i +=1
					fd.write(chunk)

			if i == 0:
				os.remove(json_dump_path.format(file_name))
				return False 
			
			return True

		except Exception as e:
			logging.error("File handling error: {}".format(e)) 
			return False

	except Exception as e:
		logging.error('Exception caught: {}'.format(e))
		return False

@misc.time_taken
def write_to_db(file_name):
	# parser = ijson.parse(open('json_data/Beachbody_products.json'))
	# res = ''
	# curr = {}
	# for prefix, event, value in parser:
	# 	if (prefix not in alternate_list) and (event == 'string'):
	# 		key = curr[value]
	# 		parser.next
	# 		curr[key] = value
	values = ""
	batch_size = C.database_batch_size
	failed = []
	with open(file_name,'r') as infile:
		for i,line in enumerate(infile):
			curr = defaultdict(lambda:'')
			line = line.strip()
			if i < 2:
				continue
			try:
				curr.update(json.loads(line[0:len(line)-1]))
			except:
				curr.update(json.loads(line[0:len(line)-2]))
			
			try:
				curr_values = "('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')".format(
					curr['product_id'],
					curr['product_name'],
					curr['product_url'],
					curr['advertiser'],
					curr['designer'],
					curr['image_url'],
					curr['price'],
					curr['commission'])
				values += curr_values
			
			except Exception as e:
				failed.append((i,curr['product_id']))
				logging.error('Something went wrong with record {0}'.format(i))
				logging.error('Reason:{0}'.format(e))
				values += ";"
				# print "run_querry with values ",values
				values = ""
				continue

			curr_values = ""
			if i%batch_size == 0:
				values += ";"
				print "run_querry with values ",values
				values = ""
			else:
				values += ","

		if len(values) > 0:
			values += ";"
			print "run_querry with values ",values
		print failed
		print len(failed)
			
# list_of_items = ['products.item.product_id','products.item.product_name','products.item.product_url',
# 				 'products.item.advertiser','products.item.designer','products.item.image_url',
# 				 'products.item.price','products.item.commission']


def add_vendor(data):
	"""
	About:
		This function is used to add a data to products table in the Postgres db

		Args: data (object of web.utils.Storage)
		Returns: Bool
	"""
	url = C.urls['vendor'].format(data.advertiser,C.secrets['admin_token'])
	file_name = json_dump_path.format(data.advertiser+'_products.json')
	
	file_created = write_response_to_file(file_name,url)

	if file_created:
		resp = misc.generate_success("File added")
		write_to_db(file_name)
	else:
		resp = misc.generate_error("Invalid Advertiser")

	return resp
