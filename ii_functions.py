#!/usr/bin/env python3

from socks import monkey_patch as socks_proxy_monkey_patch
socks_proxy_monkey_patch.monkey_patch()

import urllib.request, urllib.parse

from socks import socks_proxy_context

import os, base64, subprocess, datetime, hashlib, cgi
import paths

def applyBlackList(str):
	return str

def getMsg(msgid):
	try:
		msg=open(paths.msgdir+msgid).read().splitlines()
		tags=parseTags(msg[0])
		if('repto' in tags):
			rpt=tags['repto']
		else:
			rpt=False

		message="\n".join(msg[8:])

		meta=dict(repto=rpt,echo=msg[1],time=msg[2],sender=msg[3],addr=msg[4],to=msg[5],subj=msg[6],msg=message,id=msgid)
	except:
		meta=dict(repto=False,echo="",time=0,sender="",addr="",to="",subj="",msg="no message",id=msgid)
	return meta

def getMsgEscape(msgid): # получаем сообщение и режем html в нужных частях
	m=getMsg(msgid)
	values=["sender", "subj", "addr", "to", "msg", "repto"]
	for value in values:
		if (type(m[value]) == bool): # если repto == False (для совместимости), ибо нельзя обрабатывать не строку
			continue

		m[value]=cgi.escape(m[value], True)
	
	return m

def getOutMsg(name):
	try:
		source=open(paths.tossesdir+name).read().splitlines()
		
		str=source[4]
		if str.startswith("@repto:"):
			repto=str[7:]
			msgtext="\n".join(source[5:])
		else:
			repto=False
			msgtext="\n".join(source[4:])
		
		meta=dict(echo=source[0], to=source[1], subj=source[2], repto=repto, msg=msgtext)
	except:
		meta=dict(echo="", to="All", subj="", repto=False, msg="")
	return meta

def getOutMsgEscape(name): # получаем сообщение и режем html в нужных частях
	m=getOutMsg(name)
	values=["echo", "to", "subj", "repto", "msg"]
	for value in values:
		if (type(m[value]) == bool): # для repto
			continue

		m[value]=cgi.escape(m[value], True)
	
	return m

def getOutList():
	files=os.listdir(paths.tossesdir)
	files=[x for x in files if x.endswith(".toss") or x.endswith(".out")]
	files.sort()
	return files

def b64d(str):
	return base64.b64decode(str)

def hsh(str):
	return base64.urlsafe_b64encode( hashlib.sha256(bytes(str, "utf8")).digest() ).decode("utf8").replace('-','A').replace('_','z')[:20]

def touch(fname):
	if os.path.exists(fname):
		os.utime(fname, None)
	else:
		open(fname, 'a').close()

def savemsg(hash, echo, message):
	touch(paths.msgdir+hash)
	touch(paths.indexdir+echo)
	open(paths.msgdir+hash, "wb").write(message)
	open(paths.indexdir+echo, "a").write(hash+"\n")

def getMsgList(echo):
	if(os.path.exists(paths.indexdir+echo)):
		return open(paths.indexdir+echo).read().splitlines()
	else:
		return []

def formatDate(time):
	return datetime.datetime.fromtimestamp(int(time)).strftime("%Y-%m-%d (%A), %H:%M")

def parseTags(str):
	arr=str.split("/")
	tags={}
	for i in range(0,len(arr),2):
		if(arr[i+1]):
			tags[arr[i]]=arr[i+1]
		
	return tags
