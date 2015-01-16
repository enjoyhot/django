
from django.core.urlresolvers import reverse
from libvirt import libvirtError

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
import json
import time
import re
import sys
from servers.models import Compute

def cpuinfo():
        lines = open('/proc/stat').readlines()
        for line in lines:
    	    	ln = line.split()
	        if ln[0].startswith('cpu'):
            		return ln;
	return []
def meminfo():
        ''' Return the information in /proc/meminfo
        as a dictionary '''
	
	meminfomsg={'total':'none','free':'none'}
        with open('/proc/meminfo') as f:
		i=0
		for line in f:
			if i>1:
				break
			if i==0:
		                meminfomsg['total'] = line.split(':')[1].strip()
			if i==1:
				meminfomsg['free'] = line.split(':')[1].strip()
			i=i+1
	return meminfomsg
def cpu_mem(req):
    	points = 5
	datasets = {}
	datasets['timer']=[]
	datasets['cpurate']=[]
	datasets['memrate']=[]
	cookies = {}
	curent_time = time.strftime("%H:%M:%S")
			
        try:
        	cookies['cpurate'] = req.COOKIES.get('cpurate')
	        cookies['memrate'] = req.COOKIES.get('memrate')
	        cookies['timer'] = req.COOKIES.get('timer')
	except KeyError:
	        cookies['cpurate'] = None
	        cookies['memrate'] = None
	
        if not cookies['cpurate'] or not cookies['memrate']:
        #if not cookies['memrate']:
	        datasets['cpurate'] = [0]
        	datasets['memrate'] = [0]
	        datasets['timer'] = [curent_time]
	else:
	        datasets['cpurate'] = eval(cookies['cpurate'])
        	datasets['memrate'] = eval(cookies['memrate'])
	        datasets['timer'] = eval(cookies['timer'])
    
        datasets['timer'].append(curent_time)

	#get mem      
	
	meminfomsg = meminfo()
	pattern='(\d+).+'
	free=re.findall(pattern,str(meminfomsg['free']))
	total=re.findall(pattern,str(meminfomsg['total']))
	if free==[] or total==[]:
		free=['0']
		total=['1']
	
	memrate = (float(total[0])-float(free[0]))/float(total[0])*100
        datasets['memrate'].append(int(memrate))

	#get cpu
	
	W = cpuinfo()
	one_cpuTotal=long(W[1])+long(W[2])+long(W[3])+long(W[4])+long(W[5])+long(W[6])+long(W[7])
	one_cpuused=long(W[1])+long(W[2])+long(W[3])
	time.sleep(1)
        W = cpuinfo()
        two_cpuTotal=long(W[1])+long(W[2])+long(W[3])+long(W[4])+long(W[5])+long(W[6])+long(W[7])
        two_cpuused=long(W[1])+long(W[2])+long(W[3])
        cpuused=float(two_cpuused-one_cpuused)/(two_cpuTotal-one_cpuTotal)
        #print '%.2f%%'%(cpuused*100)
        datasets['cpurate'].append(int(cpuused*100))
	
        #datasets['cpurate'].append(50)

        if len(datasets['timer']) > points:
	        datasets['timer'].pop(0)
        if len(datasets['cpurate']) > points:
	        datasets['cpurate'].pop(0)
        if len(datasets['memrate']) > points:
        	datasets['memrate'].pop(0)
	
	
        cpu = {
	        'labels': datasets['timer'],
	        'datasets': [
                        {
    	 	        "fillColor": "rgba(241,72,70,0.5)",
	                "strokeColor": "rgba(241,72,70,1)",
	                "pointColor": "rgba(241,72,70,1)",
        	        "pointStrokeColor": "#fff",
	                "data": datasets['cpurate']
	                #"data": [12,23,34,34,45]
        	        }
	        ]
	}
	
        memory = {
                'labels': datasets['timer'],
                #'labels': '12:23',
	        'datasets': [
	         	{
	                "fillColor": "rgba(249,134,33,0.5)",
	                "strokeColor": "rgba(249,134,33,1)",
	                "pointColor": "rgba(249,134,33,1)",
	                "pointStrokeColor": "#fff",
	                "data": datasets['memrate']
	               #"data": [12,23,34,34,45]
	                }
	        ]
	}

        data = json.dumps({'cpu': cpu, 'memory': memory})
        #data = json.dumps({'memory': memory})
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
	response.cookies['cpurate'] = datasets['cpurate']
        response.cookies['timer'] = datasets['timer']
        response.cookies['memrate'] = datasets['memrate']
	response.write(data)

	return response
