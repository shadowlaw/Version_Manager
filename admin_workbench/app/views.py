#app, sqlalchemy database object and login manager object imports
from app import app, db, login_manager, file_sender

#basic flask imports
from flask import render_template, request, redirect, url_for, flash, jsonify

#login manager imports
from flask_login import login_user, logout_user, current_user, login_required

#form imports
from forms import LoginForm, NewNodeForm

#model imports for user and network nodes (machines for version control)
from models import *

#password hashing checking functions
from werkzeug.security import check_password_hash, generate_password_hash

#secure filename import
from werkzeug.utils import secure_filename

#default python package imports
import json
import os

##imports for authentication value random generation
from random import randrange
from uuid import uuid1

from utils.zipfile import *
from utils.fileManager import write, exists

################# web views #####################
#root route for main server view
@app.route('/')
def home():
	if current_user.is_authenticated:
		return redirect(url_for('dash'))

	return render_template('home.html')


#login route for main server
@app.route('/login', methods=["GET","POST"])
def login():
	
	loginForm = LoginForm() #instanciates wtforms login form
	
	if current_user.is_authenticated: #uses flask login manager to check if user is already logged in
		redirect(url_for('home'))
		
	
	if request.method == 'POST' and loginForm.validate_on_submit():
		
		user = User.query.filter_by(username=loginForm.username.data).first()
		
		if user is not None and check_password_hash(user.password, loginForm.password.data):
			
			login_user(user)
			
			flash('Logged in successfully.', 'success')
			
			next_page = request.args.get('next') #gets the url of the previous page that requires login
			
			return redirect(next_page or url_for('home')) #directs user to home page or the url retried from the next argument
		else:
			flash('Username or Password is incorrect.', 'danger')
		

	return render_template("login.html", loginForm = loginForm)

#main server dashboard route
@app.route('/dashboard')
@login_required
def dash():
	return render_template('dash.html')
	

@app.route('/add_node', methods=["GET", "POST"])
@login_required
def add_node():
	
	newNodeForm = NewNodeForm()
	
	if request.method == "POST" and newNodeForm.validate_on_submit():
		try:
			node_name = newNodeForm.node_name.data
			key=str(uuid1())
			
			new_node = Node(node_name,key)
			
			db.session.add(new_node)
			db.session.commit()
			
			return jsonify(auth_key=key)
		except Exception as e:
			print e
			db.session.rollback()
			return "Internl Error"
	
	return render_template("add_node.html", newClientForm = newNodeForm)
	
@app.route("/add_server", methods=["GET", "POST"])
@login_required
def add_server():
	
	if request.method == "POST":
		serverAddress = request.form['server_name']
		write(app.config["SERVER_LIST"], ","+serverAddress)
		
		file_sender.addIP(serverAddress)
		
		if file_sender.file_exist():
			file_sender.send(serverAddress, relativeUrl="node_list")
		
		return 'Address added'
	
	return render_template("add_server.html")

@app.route('/node_management', methods=["GET", "POST"])
@login_required
def list_nodes():
	
	if request.method == "POST":
		data = request.json
		group_name = data["name"]

		group = NodeGroup.query.filter_by(group_name = group_name).first()
		
		if group is None:
			group = NodeGroup(group_name)
			

			try:
				db.session.add(group)
				db.session.commit()
			except Exception as e:
				db.session.rollback()
				print e
					
		if data["nodes"]:
			for node in data["nodes"]:
				if node["value"] == "on":
					node = Node.query.filter_by(name = node["name"]).first()
					node.group_id = group.group_id

			try:
				db.session.commit()
			except Exception as e:
				db.session.rollback()
				print e
			
			return "Group Updated"
		
	nodes = Node.query.order_by(Node.node_id).all()
	
	gl = get_all_groups()

	assoc_sql ="select name, list_id from (select nodes.group_id, nodes.name from node_group join nodes on node_group.group_id = nodes.group_id) as A join group_list_assoc on A.group_id=group_list_assoc.group_id"
	cur=db.engine.execute(assoc_sql)
	assoc_results = cur.fetchall()
	
	other_sql = "select name from nodes where name not in (select name from (select name, list_id from (select nodes.group_id, nodes.name from node_group join nodes on node_group.group_id = nodes.group_id) as A join group_list_assoc on A.group_id=group_list_assoc.group_id) as B);"
	cur=db.engine.execute(other_sql)
	other_results = cur.fetchall()
	
	nodes=[]
	
	for item in assoc_results:
		tempDict = dict()
		tempDict["name"]=item[0]
		tempDict["list_id"]=item[1]

		nodes.append(tempDict)
	
	for item in other_results:
		nodes.append({"name": item[0]})

	return render_template("manage_nodes.html", nodes=nodes, group_list=gl)

@app.route("/node_list_assoc", methods=["GET", "POST"])
@login_required
def node_list_assoc():
	
	if request.method == "POST":
		associationArray = request.get_json()["grouping_data"]
		
		for obj in associationArray:
			group = NodeGroup.query.filter_by(group_name=obj["name"]).first()
			app_list = AppList.query.filter_by(list_id=obj["value"]).first()

			if group is not None and app_list is not None:

				assoc = GroupListAssoc(app_list.list_id, group.group_id)
				try:
					db.session.add(assoc)
					db.session.commit()
				except Exception as e:
					print e
					
				return redirect(url_for("list_nodes"))

	group_list = get_all_groups()
		
	app_list = AppList.query.order_by(AppList.list_id).all()
	
	return render_template("node_list_assoc.html", app_lists = app_list, group_lists = group_list, list_length=len(app_list))
	

@app.route("/app_list_mgmt", methods=["GET", "POST"])
@login_required
def app_list():
	
	if request.args.to_dict() != dict():
		if request.args["atn"] == "crt" and request.method == "POST":
			list_data = request.get_json()["app_data"]
			
			if list_data ==[]:
				return "Application list cannot be empty"
			
			list_name = secure_filename(request.get_json()["list_name"])
			new_app_list = dict()
			
			new_app_list["apps"] = {}
			
			for items in list_data:
				new_app_list["apps"][items["app_name"]] = items["version"]
			
			try:
				appObj = AppList(list_name)
				
				db.session.add(appObj)
				db.session.commit()
				
				
				absolute_path = generate_app_list_path(list_name)
				json.dump(new_app_list, open(absolute_path, "w"), indent=2)
				
				#===================================================
				
				app_zip = ZipFile(app.config["APP_LIST_ZIP"], "a")
				app_zip.write(absolute_path)
				app_zip.close()
				
				if not file_sender.isListEmpty():

					file_sender.send_all(relativeUrl="node_list")
					return "Application list created and sent"
				
				return "Application list created but no servers available for distribution"
			except Exception as e:
				db.session.rollback()
				print e
				return "List could not be created"
				
		elif request.args["atn"] == "crt":
			return render_template("create_app_list.html")
		
		if request.args["atn"] == "del" and request.method == "POST":
			pass
	
	app_lists = AppList.query.order_by(AppList.list_id).all()
	
	
	return render_template("display_app_list.html", app_lists = app_lists)

##############################################################

def get_all_groups():
	results = NodeGroup.query.all()
	
	group_list=[]
	
	for item in results:
		group_list.append(item.group_name)

	return group_list

def generate_app_list_path(list_name):
	return os.path.join(app.config['APP_LIST_LOCATION'], list_name+".json")

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))
	
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.errorhandler(404)
def error404(error):
	return render_template('404.html'), 404
	

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response