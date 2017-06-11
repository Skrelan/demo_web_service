import json 

def generate_error(message):
	"""
	About:
		Generates an JSON with field error

		Args: message (str)
		Returns: JSON
	"""
	resp = {'error':message}
	return json.dumps(resp)