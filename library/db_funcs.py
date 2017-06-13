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

json_dump_path = C.json_dump_path
no_key_response = C.no_key_response
got_blocked = C.got_blocked
dict_of_vendors = {}

db = web.database(dbn='postgres', 
				  db='postgres', 
				  user='postgres', 
				  pw=C.secrets["postgres"])


def query_db(query):
	"""
	About:
		This function is used to query the Postgress db
	
		Args: query (str)
		Returns: list or False
	"""
	try:
		results = db.query(query)
		return results

	except Exception as e:
		if 'FATAL:  sorry, too many clients already\n' in e:
			time.sleep(3)
			return query_db(query)

		logging.error("database connection failed\n{0}\nAborting {1}".format(e,query))
		return False


@misc.time_taken
def write_response_to_file(file_name,url):
	"""
	About:
		This function is used to added the response to a file

		Args: file_name (str), url (str)
		Returns: Bool
	"""
	r = requests.get(url,stream=True)
	try:
		with open(file_name, 'wb') as fd:
			i = 0
			for chunk in r.iter_content(chunk_size=128):	
				if i == 0:
					if no_key_response in chunk:
						logging.error(misc.generate_error(
							'Invalid Advertiser'))
						break
					if got_blocked in chunk:
						logging.error(misc.generate_error(
							'Got blocked/invalid access'))
						break
				i +=1
				fd.write(chunk)
		if i == 0:
			os.remove(file_name)
			return False
		else:
			return True

	except Exception as e:
		logging.error("File handling error: {}".format(e)) 
		return False


def insert_into_products(values):
	"""
	About:
		This function inserts the values passed to it into the database

		Args: values (str)
		Returns: None
	"""
	query = C.query['add_products'].format(values)
	try:
		r = query_db(query)
		logging.info('Query: {0} ran successfully'.format(query))
	except Exception as e:
		logging.error('Something went wrong with the query{0}'.format(query))
		logging.error('Error:{0}'.format(e))


@misc.time_taken
def write_to_db(file_name,advertiser_id):
	"""
	About:
		This function reads the locally cached file and stores it's
		contents into the database.
		Any records that fail are tracked.

		Args: file_name (str), advertiser_id (str)
		Returns: None or list
	"""
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
				curr_values = "('{0}','{1}','{2}',{3},'{4}','{5}',{6},{7})".format(
					curr['product_id'],
					curr['product_name'].encode('utf-8').replace("'","''"),
					curr['product_url'],
					advertiser_id,
					curr['designer'].encode('utf-8').replace("'","''"),
					curr['image_url'],
					float(curr['price']),
					float(curr['commission']))
				values += curr_values
			
			except Exception as e:
				failed.append([e.message,curr])
				logging.error('Something went wrong with record {0}'.format(i))
				logging.error('Reason:{0}'.format(e))
				print curr
				print values
				if len(values) > 0:
					values = values[:-1]
					values += ";"
					insert_into_products(values)
				values = ""
				continue

			curr_values = ""
			if i%batch_size == 0:
				if values[-1] == ',':
					values = values[:-1]
				values += ";"
				insert_into_products(values)
				values = ""
			else:
				values += ","

		if len(values) > 0:
			values = values[:-1]
			values += ";"
			insert_into_products(values)

		return failed if len(failed) else None


def insert_vendor(name):
	"""
	About:
		This runs the query to insert a new vendor in to
		advertiser table

		Args: name (str)
		Returns: None
	"""
	r = query_db(C.query['add_vendor'].format(name))

def get_vendor_id(name):
	"""
	About:
		This runs the query to store id of vendor
		into a gloabl dictonary - dict_of_vendors

		Args: name (str)
		Returns: None
	"""
	r = query_db(C.query['get_vendor_id'].format(name))
	if r:
		for data in r:
			dict_of_vendors[name] = data.id

@misc.time_taken
def get_vendors():
	"""
	About:
		This runs the query to store ids of all vendors
		in to a gloabl dictonary - dict_of_vendors

		Args: name (str)
		Returns: None
	"""
	r = query_db(C.query['get_vendors'])
	if r :
		for data in r:
			dict_of_vendors[data.advertiser_name] = data.id


@misc.time_taken
def add_vendor(data):
	"""
	About:
		This function is used to add a data to products table in the Postgres db

		Args: data (object of web.utils.Storage)
		Returns: Bool
	"""
	get_vendors()

	if data.advertiser in dict_of_vendors:
		resp = misc.generate_error("Advertiser already encountered")
		return resp

	url = C.urls['vendor'].format(data.advertiser,C.secrets['admin_token'])
	file_name = json_dump_path.format(data.advertiser+'_products.json')
	
	file_created = write_response_to_file(file_name,url)

	if file_created:
		insert_vendor(data.advertiser)
		get_vendor_id(data.advertiser)
		r = write_to_db(file_name,dict_of_vendors[data.advertiser])
		resp = misc.generate_success("File added",{"records that failed":r})
		os.remove(file_name)

	else:
		resp = misc.generate_error("Invalid Advertiser")

	return resp

def search_error(keyword,error_message):
	logging.error('{0} not a float'.format(keyword))
	logging.error(error_message)
	resp = misc.generate_error('{0} is not a number'.format(keyword))
	return resp


@misc.time_taken
def search_product(data):
	"""
	About:
		This function is used to search for products in products table in the database

		Args: data (web.obj)
		Returns: JSON
	"""
	where_clause = []
	extra = []

	if data.advertiser:
		where_clause.append("A.advertiser_name LIKE '%{0}%'".format(data.advertiser))
	if data.designer:
		where_clause.append("P.designer LIKE '%{0}%'".format(data.designer))
	if data.keywords:
		where_clause.append("P.product_name LIKE '%{0}%'".format(data.keywords))
	
	if data.min_price:
		try:
			m = abs(float(data.min_price))
			where_clause.append("P.price <= {0}".format(m))
		except Exception as e:
			search_error('min_price',e)

	if data.max_price:
		try:
			m = abs(float(data.max_price))
			where_clause.append("P.price >= {0}".format(m))
		except Exception as e:
			search_error('max_price',e)

	if data.limit:
		try:
			m = abs(int(data.limit))
			m = m if m < 1000 else 1000
			extra.append("LIMIT {0}".format(m))
		except Exception as e:
			search_error('limit',e)
	else:
		extra.append("LIMIT 100")

	if data.offset:
		try:
			m = abs(int(data.offset))
			m = m if m < 1000 else 1000
			extra.append("OFFSET {0}".format(m))
		except Exception as e:
			search_error('offset',e)

	if len(where_clause) == 0:
		return misc.generate_error('Missing Fields. Please send one of these [advertiser,designer,product_name,min_price,max_price,keywords]')

	query = C.query["get_products"].format(
		" AND ".join(where_clause),
		" ".join(extra))

	r = query_db(query)

	if not r:
		return json.dumps({'message':'No results found for the query'})
	else:
		data = []
		for record in r:
			temp = dict(record)
			temp['commission'] = float(record.commission)
			temp['price'] = float(record.price)
			data.append(temp)
		resp = {"result":data}
		return json.dumps(resp)
		
def load_product():
	"""
	About: This is used by the shuffle page
		Args: None
		Returns: JSON
	"""
	query = C.query["load_products"].format("LIMIT 9 OFFSET 0")
	r = query_db(query)
	if not r:
		return json.dumps({'message':'No results found for the query'})
	else:
		data = []
		for record in r:
			temp = dict(record)
			temp['commission'] = float(record.commission)
			temp['price'] = float(record.price)
			data.append(temp)
		resp = {"result":data}
		return json.dumps(resp)
	# now merege elements and make querry


