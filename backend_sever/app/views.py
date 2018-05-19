from app import app, db

from flask import jsonify, request

#model imports for user and network nodes (machines for version control)
from models import Node, AppList

#secure filename import
from werkzeug.utils import secure_filename

from utils.zipfile import *

#default python package imports
import json
import os

@app.route("/node_list", methods=["POST"])
def update_node_list():
    
	app_list =  request.files['file']
	filename = secure_filename(app_list.filename)
	
	app_list.save(os.path.join(app.config['APP_LIST_LOCATION'],filename))
	
	list_zip = ZipFile(os.path.join('./app/node_app_list', filename))
	list_zip.extractall()
	
	return ''

@app.route('/app_valid', methods = ["POST"])
def validate_cli_app():
	
	try:
		jsonObj = request.get_json()
		request_key = jsonObj['key']
	except Exception as e:
		return jsonify()
	
	
	node = Node.query.filter_by(api_key = request_key).first()
	
	if node is None:
		return jsonify()
	
	if node.node_group is None or node.app_list_id is None:
		return jsonify()
		
	set_app_list = AppList.query.filter_by(list_id = node.app_list_id).first()
	
	if set_app_list is None:
		return jsonify(message='no associated list')
	
	try:
		rec_app_list = jsonObj["apps"]
	except Exception as e:
		return jsonify(message='no list sent')
	
	file_path = generate_app_list_path(set_app_list.name)
	curr_app_list = json.load(open(file_path,"r"))['apps']  #loads list of apps from server FS
	
	curr_names = curr_app_list.keys()
	change = dict()
	to_install = dict()

	for name in curr_names:
		if rec_app_list.has_key(name): #check if the response has app key that we're looking for
			if not rec_app_list[name] == curr_app_list[name]: #if it does then it'll check the version
				change[name] = curr_app_list[name]
		else:
			to_install[name] = curr_app_list[name]
	
	return jsonify(install = to_install, changes=change) # will return new apps and versions to install and corrections to already installed applications


def generate_app_list_path(list_name):
	return os.path.join(app.config['APP_LIST_LOCATION'], list_name+".json")