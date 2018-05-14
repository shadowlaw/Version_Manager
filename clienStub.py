import time
import requests
import json
import sys


def main():
	#order of arguments
	# 1. url
	# 2. json file name
	# 3. request delay in seconds

	if len(sys.argv) < 4:
		print "Argument list:\n1. url\n2. json file name\n3. request delay in seconds"
		sys.exit(1) 	

	delay = sys.argv[3]

	url= sys.argv[1]
	jsonPayload = json.load(open(sys.argv[2], r))
	header = {"Content-Type": "application/json"}

	while True:
		response = requests.post(url, json=jsonPayload, headers=header)
		print response.status_code+"\n"
		print response.json()
		print "Delaying request for {} seconds".format(delay)
		time.sleep(delay)


if __name__ == "__main__":
	main()