import json

DATAFILE = "./control_data.json"
DOWNLOAD_DATA = "./download_data.json"

def json_read(file):
	with open(file, 'r') as jsonfile:
		data = json.load(jsonfile)
	return data


def json_write(data, file):
	with open(file, 'w') as jsonfile:
		json.dump(data, jsonfile)
		jsonfile.truncate()