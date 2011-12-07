import sqlite3
from hashlib import md5
from bottle import route, run, get, post, request, template, debug, static_file, response, redirect, error
from settings import *
#from bottle import CherryPyServer

@route('/')
@route(blogLink)
@route(blogLink[:-1])
def setup():
	con = sqlite3.connect('blog_engine.db') # Warning: This file is created in the current directory
	con.execute("CREATE TABLE IF NOT EXISTS 'posts' ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'title' varchar(32) DEFAULT NULL, 'text' text NOT NULL, 'date' date NOT NULL, 'tags' tinytext);")
	con.execute("CREATE TABLE IF NOT EXISTS  'users' ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'login' varchar(16) NOT NULL, 'email' VARCHAR(24) NOT NULL, 'pass' VARCHAR(32) NOT NULL);")
	con.execute("""INSERT INTO posts (title, text, date) VALUES('Hello :)','<p>Nice to see you. It is your first post, you can remove it or add new in admin panel</p><img src="/static/img/hello.png" />','2011/11/11');""")
	con.commit()
	con.close()
	return template('install.tpl', errorStr = 'Login')

@route('/install', method='POST')
def install():
	username = request.forms.get('login')
	password = request.forms.get('password')
	email = request.forms.get('email')
	cur = sqlite3.connect('blog_engine.db') # Warning: This file is created in the current directory
	result = cur.execute("SELECT COUNT(login) FROM users WHERE login = ?", [username.encode('utf8')]).fetchone()
	if result[0] == 0:
		submit = True
		password = md5(password.encode('utf8')).hexdigest()
		cur.execute("INSERT INTO users (login, pass, email) VALUES (?,?,?)", (username.encode('utf8'), password.encode('utf8'), email.encode('utf8')))
	else: submit = False
	cur.commit()
	cur.close()
	if submit:
		return 'delete install.py install.tpl'
		#tagString = readTags()
		#headerTags = splitHeaderTags(tagString)
		#return template('controls.tpl', siteAddress = domain, blogAddress = bAddress, tags = headerTags, pagename = sitename)
	else: return template('install.tpl',errorStr="Username " + username + " is already taken. Please choose another.")

@route('/static/:filename#.*#')
def send_file(filename):
	return static_file(filename, root=rootfolder)

def readTags():
	tagFile = open('tagsFile','r')
	tagStr = tagFile.read()
	tagFile.close()
	return tagStr
	
def splitHeaderTags(tagStr):
	tagStr = tagStr.split('\n')
	tags = {}
	if len(tagStr) > 0:
		for pair in tagStr:
			tag = pair.split(':')
			if len(tag) == 2:
				tags[tag[0]] = tag[1]
	return tags

debug(True)
#for cherrypy
#run(host=hostIP, port='80', server=CherryPyServer) 

#you can uncomment this string to debug on localhost
run(host=hostIP, port=80, server='tornado')
