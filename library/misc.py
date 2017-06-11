import json 
import logging
import time

logging.basicConfig( 
	level=logging.DEBUG,
	format="[%(asctime)s] | [%(levelname)s] | %(message)s")

def generate_error(message):
	"""
	About:
		Generates an JSON with key error

		Args: message (str)
		Returns: JSON
	"""
	resp = {'error':message}
	return json.dumps(resp)


def generate_success(message):
	"""
	About:
		Generates an JSON with key success

		Args: message (str)
		Returns: JSON
	"""
	resp = {'success':message}
	return json.dumps(resp)


def time_taken(func):
	"""
	About:
		Function that is used as a decorater, to track 
		the time taken to run a function

		Args: func (function)
		Returns: resp (response of func)
	"""
	def helper(*args,**kwargs):
		start = time.time()
		results = func(*args,**kwargs)
		end = time.time()
		diff = end - start
		logging.info("{0} function took {1} seconds".format(func.func_name,diff))
		return results
	return helper