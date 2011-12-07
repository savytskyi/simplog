import sqlite3
from datetime import datetime, timedelta
from hashlib import md5
from bottle import route, run, get, post, request, template, debug, static_file, response, redirect, error
from settings import *
from tornado import web
#from bottle import CherryPyServer

#### instruction post
#### review post
#### features/what's new post



@route('/')
@route('/:file')
def mainPage(file = 'index.html'):
	return static_file(file,rootfolder+'/mainsite/')


@route(blogLink[:-1])
@route(blogLink)
@route(blogLink + 'page-:page')
def index(page = 1):
	try:
		### this check for digits in string is so silly. need to change it
		int(page)
	except:
		return template('errorpage.tpl', pagename = sitename, blogAddress = bAddress)
	cur = connect()
	#getting numbers of pages, with X posts per page, where X=postPerPage
	all = cur.execute("SELECT COUNT(id) FROM posts").fetchone()
	allPosts = int(all[0])
	if allPosts < 1:
		return template('errorpage.tpl', pagename = sitename, blogAddress = bAddress)
	else:
		all = (allPosts / postPerPage) + 1
		if allPosts % postPerPage == 0: all -= 1
		lastPost = cur.execute("SELECT MAX(id) FROM posts").fetchone()
		lastPost = int(lastPost[0])
		lastPostOnThePage = lastPost - int(page) * postPerPage
		firstPostOnThePage = lastPostOnThePage + postPerPage
		#getting posts per present page
		result = cur.execute("SELECT id, title, text, date FROM posts WHERE id BETWEEN ? AND ? ORDER BY id DESC",(str(lastPostOnThePage+1), str(firstPostOnThePage))).fetchall()
		cur.commit()
		cur.close()
		headerTags = readTags()
		headerTags = splitHeaderTags(headerTags)
		if int(page) > int(all):
			return template('errorpage.tpl', pagename = sitename, blogAddress = bAddress)
		else:
			return template('index.tpl', siteAddress = domain, blogAddress = bAddress, tags = headerTags, pages = all, pagename = sitename, posts = result, currentPage = int(page))

@route(blogLink + 'tag/:tag')
@route(blogLink + 'tag/:tag/page-:page')
def tagsPage(tag = '', page = 1):
	try:
		int(page)
	except:
		return template('errorpage.tpl', pagename = sitename, blogAddress = bAddress, error='wrong tag page')
	if tag == '':
		return template('errorpage.tpl', pagename = sitename, blogAddress = bAddress, error='wrong tag')
	cur = connect()
	#getting numbers of pages, with X posts per page, where X=postPerPage
	rqst = "SELECT COUNT(id) FROM posts WHERE tags LIKE '%" + tag + "%'"
	all = cur.execute(rqst).fetchone()
	if int(all[0]) < 1:
		return template('errorpage.tpl', pagename = sitename, blogAddress = bAddress)
	else:
		all = int((all[0] / postPerPage) + 1)
		rqst = "SELECT MAX(id) FROM posts WHERE tags LIKE '%" + tag + "%'"
		lastPost = cur.execute(rqst).fetchone()
		lastPost = int(lastPost[0])
		lastPostOnThePage = lastPost - int(page) * postPerPage
		firstPostOnThePage = lastPostOnThePage + postPerPage
		#getting posts per present page
		rqst = "SELECT * FROM posts WHERE tags LIKE '%" + tag + "%'"
		rqst +=  " AND id BETWEEN " + str(lastPostOnThePage+1) + " AND " + str(firstPostOnThePage) + " ORDER BY id DESC"
		result = cur.execute(rqst).fetchall()
		cur.commit()
		cur.close()
		if int(page) > int(all):
			return template('errorpage.tpl', pagename = sitename, blogAddress = bAddress)
		else:
			headerTags = readTags()
			headerTags = splitHeaderTags(headerTags)
			return template('tag.tpl', siteAddress = domain, blogAddress = bAddress, tags = headerTags, pages = all, pagename = sitename, posts = result, currentPage = int(page))

@route(blogLink + 'post-:pid')
def showPost(pid):
	try:
		int(pid)
	except:
		return template('errorpage.tpl', pagename = sitename, blogAddress = bAddress)
	#####
	###geting our post for editing
	cur = connect()
	result = cur.execute("SELECT id, title, text, tags, date FROM posts WHERE id=?",[pid]).fetchone()
	cur.commit()
	cur.close()
	### for admin-style comments
	###username = request.get_cookie("username", secret = 'test'.encode('utf8'))
	if isinstance(result,tuple):
		#if everything is ok:
		headerTags = readTags()
		headerTags = splitHeaderTags(headerTags)
		return template('post.tpl', siteAddress = domain, blogAddress = bAddress, tags = headerTags,  pagename = sitename, postInfo = result)
	else:
		return template('errorpage.tpl', pagename = sitename, blogAddress = bAddress)

@route(blogLink + 'thegates')
@route(blogLink + 'thegates/')
def thegates():
	headerTags = readTags()
	headerTags = splitHeaderTags(headerTags)
	return template('thegates.tpl', siteAddress = domain, blogAddress = bAddress, tags = headerTags, errorStr = "", pagename = sitename, redirectTo = '')

@route(blogLink + 'signin', method='POST')
@route(blogLink + 'signin/:redir', method='POST')
def signin(redir = ''):
	username = request.forms.get('login')
	password = request.forms.get('password')
	cur = connect()
	result = cur.execute("SELECT pass FROM users WHERE login=?", [username.encode('utf8')]).fetchone()
	cur.close()
	headerTags = readTags()
	headerTags = splitHeaderTags(headerTags)
	if result is None:
		return template('thegates.tpl',  siteAddress = domain, blogAddress = bAddress, tags = headerTags, errorStr = 'Wrong username', pagename = sitename, redirectTo = '')
	else:
		#return md5(password.encode('utf8')).hexdigest().encode('utf8'), result[0]
		if md5(password.encode('utf8')).hexdigest().encode('utf8') == result[0]:
			#creating session key and setting cookie
			sessionKey = md5(str(datetime.now()).encode('utf8')).hexdigest()
			response.set_cookie('accInfo', username, secret = sessionKey.encode('utf8'), max_age = cookiesAge)
			#adding session key to the file
			cookieFile = open('cookieFile','w+')
			sessions = cookieFile.readlines()
			#remove previous cookie-keys for this user and adding new to the end of list
			for line in sessions:
				if line.split(':')[0] == username:
					sessions.remove(line)
			sessions.append(username+':'+sessionKey+'\n')
			cookieFile.writelines(sessions)
			cookieFile.close()
			#if redir == '':
			redirect(blogLink + 'controls')
			#else:
			#	redirect(blogLink + redir)
		else: return template('thegates.tpl',  siteAddress = domain, blogAddress = bAddress, tags = headerTags, errorStr = 'Wrong password', pagename = sitename, redirectTo = redir)

@route(blogLink + 'logout')
def logout():
	#looking for session key in file
	cookieFile = open('cookieFile','r')
	sessions = cookieFile.readlines()
	cookieFile.close()
	tagString = readTags()
	headerTags = splitHeaderTags(tagString)
	if not sessions:
		return template('thegates.tpl', siteAddress = domain, blogAddress = bAddress, tags = headerTags, errorStr = "Not logged in", pagename = sitename, redirectTo = '')
	for session in sessions:
		#if this user's cookie is exists, break the loop
		key = session.split(':')
		username = request.get_cookie("accInfo", secret = key[1][:-1].encode('utf8'))
		if username == key[0]: 
			response.delete_cookie(key[1][:-1])
			break
	return template('thegates.tpl',  siteAddress = domain, blogAddress = bAddress, tags = headerTags, errorStr = '', pagename = sitename, redirectTo = '')


@route(blogLink + 'submitPost', method='POST')
def createPost():
	postTitle = request.forms.get('title')
	postText = request.forms.get('post')
	postDate = request.forms.get('postDate')
	postTags = request.forms.get('tags')
	if len(postTags) > 0 and postTags != ' ':
		postTags = splitTags(postTags)
	else: postTags = ''
	cur = connect()
	lastPost = cur.execute("SELECT MAX(id) FROM posts").fetchone()
	lastPost = int(lastPost[0])
	cur.execute("INSERT INTO posts (id, title, text, tags, date) VALUES(?,?,?,?,?)",(lastPost + 1,postTitle.encode('utf8'), postText.encode('utf8'), postTags.encode('utf8'), postDate))
	cur.commit()
	cur.close()
	redirect(blogLink)

@route(blogLink + 'editpost-:pid')
def editpost(pid):
	#####
	try:
		### this checking for digits in string is so silly. need to change it
		int(pid)
	except:
		return template('errorpage.tpl', pagename = sitename, blogAddress = bAddress)
	#####
	###geting our post for editing
	#looking for session key in file
	cookieFile = open('cookieFile','r')
	sessions = cookieFile.readlines()
	cookieFile.close()
	tagString = readTags()
	headerTags = splitHeaderTags(tagString)
	if not sessions:
		return template('thegates.tpl', siteAddress = domain, blogAddress = bAddress, tags = headerTags, errorStr = "User is not logged", pagename = sitename, redirectTo = 'editpost-' + pid)
	for session in sessions:
		#if this user's cookie is exists, break the loop
		key = session.split(':')
		username = request.get_cookie("accInfo", secret = key[1][:-1].encode('utf8'))
		if username == key[0]: break
	if username:
		cur = connect()
		result = cur.execute("SELECT id, title, text, tags, date FROM posts WHERE id=?",[pid]).fetchone()
		cur.commit()
		cur.close()
		if isinstance(result,tuple):
			#if everything is ok:
			tagString = readTags()
			headerTags = splitHeaderTags(tagString)
			return template('editor.tpl', siteAddress = domain, blogAddress = bAddress, tags = headerTags,  pagename = sitename, postInfo = result, hTags = tagString)
		else:
			#return error page
			return template('errorpage.tpl', pagename = sitename, blogAddress = bAddress)
	else:
		return template('thegates.tpl', siteAddress = domain, blogAddress = bAddress, tags = headerTags, errorStr = "Session is closed", pagename = sitename, redirectTo = 'editpost-' + pid)

@route(blogLink + 'savepost-:pid', method="POST")
def savePost(pid):
	#####
	try:
		### this checking for digits in string is so silly. need to change it
		int(pid)
	except:
		return template('errorpage.tpl', pagename = sitename, blogAddress = bAddress)
	##### 
	###geting our post for editing
	cur = connect()
	title = request.forms.get('title')
	text = request.forms.get('post')
	#text = request.forms.get('editor')
	date = request.forms.get('postDate')
	postTags = request.forms.get('tags')
	if len(postTags) > 0 and postTags != ' ':
		postTags = splitTags(postTags)
	else: postTags = ''
	cur.execute("UPDATE posts SET title=?, text=?, tags=?, date=? WHERE id=?",(title.encode('utf8'),text.encode('utf8'),postTags.encode('utf8'),date,pid))
	### code
	cur.commit()
	cur.close()
	### return to main page
	redirect(blogLink)

@route(blogLink + 'delete-:pid')
def delete(pid):
	#####
	try:
		### this checking for digits in string is so silly. need to change it
		int(pid)
	except:
		return template('errorpage.tpl', pagename = sitename, blogAddress = bAddress)
	#####
	###geting our post for editing
	cur = connect()
	cur.execute("DELETE FROM posts WHERE id=?",[pid])
	### code
	cur.commit()
	cur.close()
	### return to main page
	redirect(blogLink)

@route(blogLink + 'controls')
@route(blogLink + 'controls/')
def controls():
	#looking for session key in file
	cookieFile = open('cookieFile','r')
	sessions = cookieFile.readlines()
	cookieFile.close()
	tagString = readTags()
	headerTags = splitHeaderTags(tagString)
	if not sessions:
		return template('thegates.tpl', siteAddress = domain, blogAddress = bAddress, tags = headerTags, errorStr = "", pagename = sitename, redirectTo = '')
	for session in sessions:
		#if this user's cookie is exists, break the loop
		key = session.split(':')
		username = request.get_cookie("accInfo", secret = key[1][:-1].encode('utf8'))
		if username == key[0]: break
	if username:
		return template('controls.tpl',  siteAddress = domain, blogAddress = bAddress, tags = headerTags, pagename = sitename, hTags = tagString)
	else:
		return template('thegates.tpl', siteAddress = domain, blogAddress = bAddress, tags = headerTags, errorStr = "", pagename = sitename, redirectTo = '')

@route(blogLink + 'postListFrom-:pid')
@route(blogLink + 'postListFrom')
def postList(pid = 0):
	#####
	try:
		### this check for digits in string is so silly. need to change it
		int(pid)
	except:
		return template('errorpage.tpl', pagename = sitename, blogAddress = bAddress)
	cur = connect()
	#getting numbers of pages, with X posts per page, where X=postPerPage
	lastPost = cur.execute("SELECT MAX(id) FROM posts").fetchone()
	lastPost = int(lastPost[0]) - int(pid)*10
	lastPostOnThePage = lastPost - 10
	lastPage = False
	firstPage = False
	if int(pid) == 0: firstPage = True
	if lastPostOnThePage < 0: lastPage = True
	#firstPostOnThePage = lastPostOnThePage + postPerPage
	#getting posts per present page
	result = cur.execute("SELECT id, title, text, date FROM posts WHERE id BETWEEN ? AND ? ORDER BY id DESC",(str(lastPostOnThePage), str(lastPost))).fetchall()
	cur.commit()
	cur.close()
	#if int(page) > int(all):
	#	return template('errorpage.tpl', pagename = sitename, blogAddress = bAddress)
	#else: 

	return template('view.tpl', lP = lastPage, fP = firstPage, siteAddress = domain, blogAddress = bAddress, previousPost = int(pid) - 1, nextPost = int(pid) + 1, posts = result)
	####

@route(blogLink + 'addTags', method='POST')
def addTags():
	tags = request.forms.get('headerTags')
	tags = makeHeaderTags(tags)
	tagFile = open('tagsFile','w')
	tagFile.write(tags)
	tagFile.close()
	redirect(blogLink)

@route('/static/:filename#.*#')
def send_file(filename):
	return static_file(filename, root=rootfolder)

def connect():
	sqliteConnect = sqlite3.connect('blog_engine.db') # Warning: This file is created in the current directory
	return sqliteConnect

def splitTags(tagString):
	if tagString != 'Tags. Please separate tags with coma' and tagString != 'None':
		tags = tagString.split(',')
		newTagString = ''
		for tag in tags:
			#removing spaces from tag beginning
			while tag[0] == ' ':
				tag = tag[1:]
			#removing spaces from tag ending
			while tag[len(tag)-1] == ' ':
				tag = tag[:-1]
			tag += ','
			newTagString += tag
		return newTagString[:-1]
	else:
		return ''

def makeHeaderTags(tags):
	tags = tags.split('\n');
	tagStr = ''
	if len(tags) > 0:
		for pair in tags:
			tag = pair.split(':');
			if len(tag) == 2:
				for word in tag:
					while word[0] == ' ':
						word = word[1:]
					while word[len(word)-1] == ' ':
						word = word[:-1]
				tagStr += tag[0]+':'+tag[1]+'\n'
	return tagStr

def readTags():
	tagFile = open('tagsFile','r')
	tagStr = tagFile.read()
	tagFile.close()
	return tagStr

def splitHeaderTags(tagStr):
	symbols = """,./\|*^%;"'"""
	tagStr = tagStr.split('\n')
	tags = {}
	if len(tagStr) > 0:
		for pair in tagStr:
			tag = pair.split(':')
			if len(tag) == 2:
				for symbol in symbols:
					tag[0] = tag[0].replace(symbol,'')
					tag[1] = tag[1].replace(symbol,'')
				tags[tag[0]] = tag[1]
	return tags
	
"""@error(404)
@error(403)
def err(code):
    return template'There is something wrong!'
"""
debug(True)
#for cherrypy
#run(host=hostIP, port='80', server=CherryPyServer) 

#you can uncomment this string to debug on localhost
run(host=hostIP, port=80, server='tornado')
