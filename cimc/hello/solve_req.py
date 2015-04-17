from hello.models import *
from django.http import HttpResponseRedirect
import pymongo
from django.http import HttpResponse
import time
import hashlib
import pexpect,thread,os
from cimc2.settings import route_from,route_to,remotepasswd,remoteuser,remotehost,remoteport

def custom_proc(req):
        "a context processor that provide something for base.html"
        admin_name = req.user['username']
        return {'admin_name':admin_name}

def transfer_time(timestamp):
	time_array=time.localtime(timestamp)
	result_time=time.strftime("%Y-%m-%d %H:%M:%S",time_array)
	return result_time
def cimc_user_req(req):
	if req.is_ajax():
		#set or get the new user message
		username=req.POST['username']
		password=req.POST['password']
		email=req.POST['email']
		status=2
		recordtype=int(float(req.POST['recordtype']))
		recordname=req.POST['recordname']
		recordcode=req.POST['recordcode']
		recordtelphone=int(float(req.POST['recordtelphone']))
		recordcompany=req.POST['recordcompany']
		recordaddress=req.POST['recordaddress']
		regtime=int(time.time())
		newuserid='userid'
		tmp=cimc_user.objects.order_by("-userid").first()
		if tmp !=None:
			newuserid=tmp.userid+1
		else:
			newuserid=1
		#newuserid=1
		#create the object
		newuser=cimc_user(
			userid=newuserid,
			password=password,
			username=username,
			email=email,
			regtime=int(time.time()),
			status=2,
			recordname=recordname,
			recordcode=recordcode,
			recordtelphone=recordtelphone,
			recordcompany=recordcompany,
			recordaddress=recordaddress,
			recordtype=recordtype
			)
		#insert to cimc_user
		newuser.insert()
	if req.method=='POST' and not req.is_ajax():
		pass_con=req.POST.get('content','')
		notpass_con=req.POST.get('content2','')	
		recover_con=req.POST.get('content3','')
		#handle review	
		if pass_con != '':
			value=pass_con.split(',')
			for item in value:
				#insert/update msg to cimc_message 
				msg={'msg_from':'admin','to':int(float(item)),'msg_type':'1','time':int(time.time()),'status':0,'result':1}
				cimc_message_update(**msg)
				#change the status of cimc_user after review
				cimc_user_update(int(float(item)),2)

		elif notpass_con != '':
			value=notpass_con.split(',')
			for item in value:
				#insert/update msg to cimc_message 
				msg={'msg_from':'admin','to':int(float(item)),'msg_type':'1','time':int(time.time()),'status':0,'result':1}
				cimc_message_update(**msg)
				#change the status of cimc_user after review
				cimc_user_update(int(float(item)),-1)
		elif recover_con != '':
			value=recover_con.split(',')
			for item in value:
				#insert/update msg to cimc_message 
				msg={'to':int(float(item)),'msg_type':'1','status':0}
				cimc_message_delete(**msg)
				#change the status of cimc_user after review
				cimc_user_update(int(float(item)),1)
def cimc_midware_req(req):
	if req.method=='POST'and not req.is_ajax():
		#review_midware
		pass_review_con=req.POST.get('content','')
		notpass_review_con=req.POST.get('content2','')	
		
		#test file
		pass_test_con=req.POST.get('content4','')
		notpass_test_con=req.POST.get('content5','')	

		#recover
		recover_con=req.POST.get('content3','')	

		# review the midware users
		if pass_review_con != '':
			value=pass_review_con.split(',')
			for item in value:
				user_id=''
				for user_item in cimc_midware.objects(midwareid=int(float(item))):
					user_id=user_item['userid']

				#insert/update msg to cimc_message 
				msg={'msg_from':'admin','to':user_id,'msg_type':'4','time':int(time.time()),'status':0,'result':1,'midwareid':int(float(item))}
				cimc_message_update(**msg)
				#change the status of cimc_user after review
				cimc_midware_update(user_id,1)
		elif notpass_review_con != '':
			value=notpass_review_con.split(',')
			for item in value:
				user_id=''
				user_item=cimc_midware.objects(midwareid=int(float(item))).first()
				user_id=user_item.userid
				#number_item=cimc_device.objects(deviceid=int(float(serial_deviceid)),level=3).first()
				msg={'msg_from':'admin','to':user_id,'msg_type':'4','time':int(time.time()),'status':0,'result':0,'midwareid':int(float(item))}
				cimc_message_update(**msg)
				cimc_midware_update(user_id,-1)

		#test the midware files
		elif pass_test_con != '':
			value=pass_test_con.split(',')
			for item in value:
				user_id=''
				for user_item in cimc_midware.objects(midwareid=int(float(item))):
					user_id=user_item['userid']

				#change the status of cimc_user after review
				cimc_midware_update(user_id,2)

				#start a thread to move file

				user_item=cimc_midware.objects(midwareid=int(float(item))).first()
				route_from=user_item.path
				thread.start_new_thread(scp_to,(route_from,remoteuser,remotehost,route_to,remotepasswd))

		elif notpass_test_con != '':
			value=notpass_con.split(',')
			for item in value:
				user_id=''
				user_item=cimc_midware.objects(midwareid=int(float(item))).first()
				user_id=user_item.userid
				#number_item=cimc_device.objects(deviceid=int(float(serial_deviceid)),level=3).first()
				cimc_midware_update(user_id,-1)
		#revover
		elif recover_con != '':
			value=recover_con.split(',')
			for item in value:
				user_id=''
				user_item=cimc_midware.objects(midwareid=int(float(item))).first()
				user_id=user_item.userid				
				msg={'to':user_id,'msg_type':'4','midwareid':int(float(item))}
				cimc_message_delete(**msg)
				cimc_midware_update(user_id,0)
		else:
			mid_message=req.POST.get('mid_message','')	
			userid=''
			devicecompany=''
			middlewarename=''
			midwareversion=''
			midwaremsg=''
			devicetype=''
			if mid_message!='':
				value=mid_message.split(',')
				userid=value[0]
				devicecompany=value[1]
				middlewarename=value[2]
				midwareversion=value[3]
				midwaremsg=value[4]
				devicetype=value[5]
			f=req.FILES['docfile']
			name=f.name
			filesize=f.size	
			#path='/home/gugugujiawei/DjangoServer/cimc/'+value[2]+'.cgi'
			path=route_from+value[2]+'.cgi'
			md5=handle_uploaded_file(f,path,filesize)
			i=cimc_midware.objects.order_by('-midwareid').first()
			if i!=None:
				midwareid=i.midwareid+1
			else:
				midwareid=1
			newmidware=cimc_midware(
				middlewarename=middlewarename,
				devicecompany=devicecompany,
				devicetype=devicetype,
				userid=int(float(userid)),
				midwareversion=midwareversion,
				midwaremsg=midwaremsg,
				size=filesize,
				path=path,
				uploadtime=int(time.time()),
				md5=md5,status=1,urlapi='api',logpath='logpath',
				totalcount=1111,successcount=1111,
				midwareid=midwareid
				)
			newmidware.insert()
# handle upload file
def handle_uploaded_file(f,path,size):
	with open(path,'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
		md5=''
		if size>20000:
			myhash=hashlib.md5()
			while True:
				b=destination.read(8096)
				if not b:
					break	
				myhash.update(b)
			md5=myhash.hexdigest
		else:
			md5obj=hashlib.md5()
			md5obj.update(f.read())
			md5=md5obj.hexdigest()
		return str(md5)
		destination.close()

# move midware file to remote server
def scp_to(route_from,user,host,route_to,password):  
    cmd = "scp -P %s %s %s@%s:%s"%(remoteport,route_from,user,host,route_to)  
    print cmd  
    scp = pexpect.spawn(cmd)  
    try:  
        i = scp.expect(['password:',pexpect.EOF],timeout=60)  
        if i == 0:  
            scp.sendline(password)  
            j = scp.expect(['password:',pexpect.EOF],timeout=60)  
            if j == 0:  
                print "password wrong for %s for %s"%(user,host)
    except:  
        print 'error'
    scp.close() 

def cimc_device_req(req):
	if req.is_ajax():
		ajax_type=req.POST['type']
		if ajax_type=='1':		
			serial_str=req.POST['serialnumber']
			serial_deviceid=req.POST['deviceid']
			serial_list=serial_str.split('/')
			cimc_device_id(int(float(serial_deviceid)),*serial_list)
			#set the message
			number_item=cimc_device.objects(deviceid=int(float(serial_deviceid)),level=3).first()
			userid=number_item.userid
			devicenumber=number_item.devicenumber
			msg={'msg_from':'admin','to':userid,'msg_type':'5','time':int(time.time()),'status':0,'result':1,'devicenumber':devicenumber}
			cimc_message_update(**msg)
			return None
		elif ajax_type=='2':
			rec_userid=req.POST['userid']
			devicecompany=req.POST['devicecompany']
			devicetype=req.POST['devicetype']
			chaintype=req.POST['chaintype']
			chain_list=chaintype.split(',')
			deviceid_level1=''
			deviceid_level2=''
			ii=cimc_device.objects(level=1).order_by('-deviceid').first()
			if ii!=None:
				deviceid_level1=ii.deviceid+1
			else:
				deviceid_level1=1
			ii=cimc_device.objects(level=2).order_by('-deviceid').first()
			if ii!=None:
				deviceid_level2=ii.deviceid+1
			else:
				deviceid_level2=1
			
			message_level1=cimc_device(
				deviceid=deviceid_level1,
				userid=int(float(rec_userid)),
				devicecompany=devicecompany,
				count=1,
				pid=0,
				level=1,
				status=2,
				recordtime=int(time.time())
				)
			if not cimc_device.objects(userid=int(float(rec_userid)),devicecompany=devicecompany):
				message_level1.insert()
			pid1='pid'
			ii=cimc_device.objects(level=1,userid=int(float(rec_userid))).first()
			if ii == None:
				pid1=1
			else:
				pid1=ii.deviceid
			message_level2=cimc_device(
				level=2,
				devicetype=devicetype,
				deviceid=deviceid_level2,
				userid=int(float(rec_userid)),	
				devicecompany=devicecompany,
				count=1,
				pid=pid1,
				status=2,
				recordtime=int(time.time()),
				chaintype=chain_list
				)
			if cimc_device.objects(userid=int(float(rec_userid)),devicetype=devicetype,devicecompany=devicecompany,level=2).count()==0:
				message_level2.insert()
			return None
		elif ajax_type=='3':
			rec_userid=req.POST['userid']
			devicecompany=req.POST['devicecompany']
			devicetype=req.POST['devicetype']
			serialnumber=req.POST['serialnumber']
			serial_list=serialnumber.split('/')
			deviceid=0
			devicenumber=''
			chaintype=''

			ii=cimc_device.objects(level=3).order_by('-deviceid').first()
			if ii!=None:
				deviceid=ii.deviceid+1
			else:
				deviceid=1

			ii=cimc_device.objects(level=2,devicecompany=devicecompany).first()
			if ii!=None:
				pid=ii.deviceid
			else:
				pid=1
			chaintype=ii.chaintype

			devicenumber='cimc-'+devicetype+'-'+str(int(time.time()))
			message_level3=cimc_device(
				deviceid=deviceid,
				devicenumber=devicenumber,
				userid=int(float(rec_userid)),
				devicecompany=devicecompany,
				devicetype=devicetype,
				pid=pid,
				level=3,
				status=2,
				recordtime=int(time.time()),
				updatetime=int(time.time()),
				serialnumber=serial_list,
				chaintype=chaintype,
				)
			message_level3.location['longtitude']=100
			message_level3.location['latitude']=200
			if cimc_device.objects(userid=int(float(rec_userid)),serialnumber=serial_list,level=3).count()==0:
				message_level3.insert()
			return None
		elif ajax_type=='4':
			str1='<option value='
			str2='</option>'
			strall=''
			for item in cimc_device.objects(level=1):
				strall=strall+str1+item.devicecompany+'>'+item.devicecompany+str2
		#	return HttpResponse(strall)
			return strall
		elif ajax_type=='5':
			str1='<option value='
			str2='</option>'
			strall=''
			devicecompany=req.POST['devicecompany']
			for item in cimc_device.objects(level=2,devicecompany=devicecompany):
				strall=strall+str1+item.devicetype+'>'+item.devicetype+str2
		#	return HttpResponse(strall)
			return strall
			
	if req.method=='POST' and not req.is_ajax():
		pass_company_con=req.POST.get('content','')
		notpass_company_con=req.POST.get('content2','')	
		pass_bind_con=req.POST.get('content3','')
		notpass_bind_con=req.POST.get('content4','')	
		recover_con=req.POST.get('content5','')	
		recover_bind=req.POST.get('content6','')	
		if pass_company_con != '':
			value=pass_company_con.split(',')
			for item in value:
				device_type=''
				userid='id'
				username='name'
				device_item=cimc_device.objects(deviceid=int(float(item)),level=2).first()
				user_id=device_item.userid
				device_type=device_item.devicetype

				msg={'msg_from':'admin','to':user_id,'msg_type':'2','time':int(time.time()),'status':0,'result':1,'devicetype':device_type}
				cimc_message_update(**msg)
				#change the status of cimc_device after review
				cimc_device_update(int(float(item)),level=2,status=2)

				
		elif notpass_company_con != '':
			value=notpass_company_con.split(',')
			for item in value:
				device_type=''
				userid=0
				device_item=cimc_device.objects(deviceid=int(float(item)),level=2).first()
				userid=device_item.userid
				devicetype=device_item.devicetype
				msg={'msg_from':'admin','to':userid,'msg_type':'2','time':int(time.time()),'status':0,'result':0,'devicetype':devicetype}
				cimc_message_update(**msg)
				#change the status of cimc_device after review
				cimc_device_update(int(float(item)),level=2,status=-1)

		elif pass_bind_con != '':
			value=pass_bind_con.split(',')
			for item in value:
				device_number=''
				userid='id'
				number_item=cimc_device.objects(deviceid=int(float(item)),level=3).first()
				userid=number_item.userid
				devicenumber=number_item.devicenumber
				msg={'msg_from':'admin','to':userid,'msg_type':'3','time':int(time.time()),'status':0,'result':1,'devicenumber':devicenumber}
				cimc_message_update(**msg)
				#change the status of cimc_device after review
				cimc_device_update(int(float(item)),level=3,status=2)
		elif notpass_bind_con != '':
			value=notpass_bind_con.split(',')
			for item in value:
				device_number=''
				userid=0
				number_item=cimc_device.objects(deviceid=int(float(item)),level=3).first()
				userid=number_item.userid
				devicenumber=number_item.devicenumber
				msg={'msg_from':'admin','to':userid,'msg_type':'3','time':int(time.time()),'status':0,'result':0,'devicenumber':devicenumber}
				cimc_message_update(**msg)
				#change the status of cimc_device after review
				cimc_device_update(int(float(item)),level=3,status=-1)
		elif recover_con != '':
			value=recover_con.split(',')
			for item in value:
				userid='id'
				device_type=''
				item_item=cimc_device.objects(deviceid=int(float(item))).first()
				userid=item_item.userid
				devicetype=item_item.devicetype	
				msg={'to':userid,'msg_type':'2','devicetype':item_item.devicetype}
				cimc_message_delete(**msg)
				cimc_device_update(int(float(item)),level=2,status=1)
		elif recover_bind != '':
			value=recover_bind.split(',')
			for item in value:
				userid='id'
				device_type=''
				item_item=cimc_device.objects(deviceid=int(float(item))).first()
				userid=item_item.userid
				devicetype=item_item.devicetype	
				msg={'to':userid,'msg_type':'3','devicenumber':item_item.devicenumber}
				cimc_message_delete(**msg)
				cimc_device_update(int(float(item)),level=3,status=1)
		returnmsg=None
		return returnmsg

