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
		Returns: list or None
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
		return None