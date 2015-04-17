#coding:utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from hello.authentication import *
from django.http import HttpResponse
from hello.models import *
from hello.server_info_req import *
from hello.solve_req import custom_proc
import time
#need for server_info
import socket
import uuid
import platform
import os,re,urllib2
from cimc2.settings import TIME_JS_REFRESH
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

#if has no public ip,return the gateway addr
class Get_public_ip:
    def getip(self):
        try:
            myip = self.visit("http://www.whereismyip.com/")
        except:
            try:
                myip = self.visit("http://www.ip138.com/ip2city.asp")
            except:
                myip = "So sorry!!!"
        return myip
    def visit(self,url):
        opener = urllib2.urlopen(url)
        if url == opener.geturl():
            str = opener.read()
        return re.search('\d+\.\d+\.\d+\.\d+',str).group(0)
ipdict=[]

@login_required
@csrf_exempt
def server_info(req):
	returnmsg = server_info_req(req)
	#get ip mac
	macobj=uuid.UUID(int=uuid.getnode()).hex[-12:]
	mac=':'.join([macobj[e:e+2] for e in range(0,11,2)])
	server_name=socket.getfqdn(socket.gethostname())
	'''
	try:
        	csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        	csock.connect(('8.8.8.8', 80))
        	(addr, port) = csock.getsockname()
        	csock.close()
        	ip=addr
        except socket.error:
        	ip="127.0.0.2"
	'''
	getmyip=Get_public_ip()
	ip=getmyip.getip()
	networkmsg={'mac':mac,'server_name':server_name,'ip':ip}

	#get system
	msg=platform.uname()
	versionmsg={'version':msg[0],'server_name':msg[1],'versionid':msg[2]}

	#get load_state
   	loadavg = {} 
        f = open("/proc/loadavg") 
        con = f.read().split() 
        f.close() 

	loadavg={'lavg_15':con[2],'rate':con[3],'last_pid':con[4]}

	#get ip
	ipobjects=cimc_ip.objects
	global ipdict
	ipdict=[]
	for item in ipobjects:	
		ipdict.append({'ip':item.ip})	
	ip_length=len(ipdict)
	return render_to_response('server-info.html',{'networkmsg':networkmsg,'versionmsg':versionmsg,'loadavg':loadavg,'time_refresh':TIME_JS_REFRESH*2,'ip_con':ipdict,'ip_length':ip_length},context_instance=RequestContext(req,processors=[custom_proc]))

def get_status(req):
	global ipdict
	data={
		'status':[]
	}
	
	for item in ipdict:
		pingmsg=os.system('ping -c 1 %s > /dev/null 2>&1' % item['ip'])
		if pingmsg == 0:
			data['status'].append('Alive')
		else:
			data['status'].append('Unknown')
		
	if data['status']==[]:
		data['status']=['none']
        datas = json.dumps({'data': data})
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
	response.write(datas)
        return response
