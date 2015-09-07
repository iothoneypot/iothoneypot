#!/usr/bin/python

import web
import re
import base64
import datetime
import cgi

cgi.maxlen = 10 * 1024 * 1024 #10MB
web.config.debug = False

name = ''
word = ''
prev_url = ''

urls = (
    '/home','Home',
    '/','Login',
    '/settings','Settings',
    '/video','Video',
    '/restart','Restart',
    '/uploading','Uploading'
)

app = web.application(urls, globals())

allowed = (
    ('mycam','p@ssw0rd63'),
    ('admin','password')
)

class Settings:
    def GET(self):
        global prev_url
        ipaddr = web.ctx['ip']
        with open("log", "a") as logfile:
                    current_time = str(datetime.datetime.now())
                    logfile.write("\n" + current_time + "\tHost:" + ipaddr)
                    logfile.write("\n(Redirected to Settings from: " + prev_url + ")\n")
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
           settings = open('settings','r')
           prev_url = "Settings"
           return settings
        else:
           raise web.seeother('/')
    
    def POST(self):
	data=web.data()
	ipaddr = web.ctx['ip']
        with open("log", "a") as logfile:
                    current_time = str(datetime.datetime.now())
                    logfile.write("\n" + current_time + "\tHost:" + ipaddr)
		    logfile.write("\n(Attempted Settings change with string:)\n" + data + "\n")
        	    raise web.seeother('/settings')
        if web.ctx.env.get('HTTP_AUTHORIZATION') is None:
           raise web.seeother('/')

class Uploading:
    def POST(self):
	ipaddr = web.ctx['ip']
	global prev_url
        prev_url = "Uploaded"
	x = web.input(myfile={})
	print ValueError
        filedir = '/root/Desktop/uploads' # Storage directory
        if 'myfile' in x: # to check if the file-object is created
        	filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
        	filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
		fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
            	fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
          	fout.close() # closes the file, upload complete.
		with open("log", "a") as logfile:
                    current_time = str(datetime.datetime.now())
                    logfile.write("\n" + current_time + "\tHost:" + ipaddr)
                    logfile.write("\nFile: (" + filename + ") Uploaded\n")
	return """<html><head></head><body>Success. System will be updated shortly.<br/><form><input type="button" value="Click to go back" onClick="history.go(-1);return true;"></form><br/></body></html>"""

class Login:
    def GET(self):
        global prev_url
        prev_url = "Login"
        auth = web.ctx.env.get('HTTP_AUTHORIZATION')
        authreq = False
        
	if auth is None:
            authreq = True
        else:
            auth = re.sub('^Basic ','',auth)
            try:
                username,password = base64.decodestring(auth).split(':')
	        global name
	        name = username
	        global word
	        word = password
            except TypeError, e:
                with open("error.txt", "a") as errorfile:
                        current_time = str(datetime.datetime.now())
                        errorfile.write("\n" + current_time + e)
            else:
		user_agent = web.ctx.env['HTTP_USER_AGENT']
		current_time = str(datetime.datetime.now())		
		ipaddr = web.ctx['ip']

                if (username,password) in allowed:
	            with open("log", "a") as logfile:                      
                        logfile.write("\n" + current_time + "\tHost:" + ipaddr)
                        logfile.write("\nBy User Agent: " + user_agent)
                        logfile.write("\n(Login Succeeded)\n")
                    raise web.seeother('/settings')
		
                else:
                    authreq = True
                    with open("log", "a") as logfile:                              
                        logfile.write("\n" + current_time + "\tHost:" + ipaddr)
                        logfile.write("\nUser Agent: " + user_agent)
                        logfile.write("\n(Login Failed)")
                        logfile.write("\nUsername: " + username + "\tPassword: " + password + "\n")
			print web.ctx['ip']
			print web.ctx.env['REQUEST_METHOD']
			
        if authreq:
            web.header('WWW-Authenticate','Basic realm="Access Denied"')
            web.ctx.status = '401 Unauthorized'
            return

if __name__=='__main__':
    app.run()