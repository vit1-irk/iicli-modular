#!/usr/bin/env python3

from ii_functions import *
import paths

def getfile(file, quiet=False):
	if (not quiet):
		print("fetch "+file)
	return urllib.request.urlopen(file).read().decode("utf8")

def parseFullEchoList(echobundle):
	echos2d={}
	echobundle=echobundle.splitlines()
	lastecho=""

	for element in echobundle:
		if element:
			if "." not in element:
				echos2d[lastecho].append(element)
			else:
				lastecho=element
				echos2d[lastecho]=[]
	return echos2d

def fetch_messages(adress, firstEchoesToFetch, xcenable=False, one_request_limit=20, fetch_limit=False, from_msgid=False):
	if(len(firstEchoesToFetch)==0):
		return []
	if(xcenable):
		xcfile=paths.datadir+"base-"+hsh(adress)
		donot=[]
		try:
			f=open(xcfile).read().splitlines()
		except:
			touch(xcfile)
			open(xcfile, "w").write("\n".join([x+":0" for x in firstEchoesToFetch]))
			f=False
		if(f):
			remotexcget=getfile(adress+"x/c/"+"/".join(firstEchoesToFetch))
			remotexc=[x.split(":") for x in remotexcget.splitlines()]
			
			if(len(f)==len(remotexc)):
				xcdict={}
				for x in remotexc:
					xcdict[x[0]]=int(x[1])
				localdict={}
				for x in [i.split(":") for i in f]:
					localdict[x[0]]=int(x[1])
			
				for echo in firstEchoesToFetch:
					if int(xcdict[echo])==int(localdict[echo]):
						donot.append(echo)
						print("removed "+echo)
				
			open(xcfile, "w").write(remotexcget)
			
		echoesToFetch=[x for x in firstEchoesToFetch if x not in donot]
	else:
		echoesToFetch=firstEchoesToFetch

	if(len(echoesToFetch)==0):
		return []
	
	if (fetch_limit != False):
		echoBundle=getfile(adress+"u/e/"+"/".join(echoesToFetch)+"/-"+str(fetch_limit)+":"+str(fetch_limit))
	else:
		echoBundle=getfile(adress+"u/e/"+"/".join(echoesToFetch))
	
	remoteEchos2d=parseFullEchoList(applyBlackList(echoBundle))
	savedMessages=[]
	
	for echo in echoesToFetch:
		localMessages=getMsgList(echo)
		
		remoteMessages=remoteEchos2d[echo]

		difference=[i for i in remoteMessages if i not in localMessages]
		difference2d=[difference[i:i+one_request_limit] for i in range(0, len(difference), one_request_limit)]
		
		for diff in difference2d:
			print(echo)
			impldifference="/".join(diff)
			fullbundle=getfile(adress+"u/m/"+impldifference)
	
			bundles=fullbundle.splitlines()
			for bundle in bundles:
				arr=bundle.split(":")
				if(arr[0]!="" and arr[1]!=""):
					msgid=arr[0]; message=b64d(arr[1])
					print("savemsg "+msgid)
					savedMessages.append(msgid)
					savemsg(msgid, echo, message)
	return savedMessages
