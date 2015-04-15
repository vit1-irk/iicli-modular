#!/usr/bin/env python2
# -*- coding:utf8 -*-

from ii_functions import *
from getcfg import *

def sendMessages():
	files=os.listdir("out")
	files=[x[:-5] for x in files if x.endswith(".toss")]
	files.sort()
	
	countsent=0
	for file in files:
		f=open("out/"+file+".toss").read()
		
		adress=servers[0]["adress"]
		authstr=servers[0]["authstr"]

		for server in servers:
			if(f.splitlines()[0] in server["echoareas"]):
				adress=server["adress"]
				authstr=server["authstr"]
				break
		
		code=base64.b64encode(f)
		
		data = urllib.urlencode({'tmsg': code,'pauth': authstr})
		print adress
		print authstr
		out = urllib.urlopen(adress + 'u/point', data).read()
		print out
		
		if out.startswith('msg ok'):
			countsent+=1
			os.rename("out/"+file+".toss", "out/"+file+".out")
	return countsent
