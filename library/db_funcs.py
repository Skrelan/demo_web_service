import web
import config.configs as configs
import logging

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

