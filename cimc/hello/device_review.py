#coding:utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from hello.forms import UploadFileForm
from hello.models import *
from hello.solve_req import *
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import time
import hashlib
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from hello.paging import get_page_msg

@login_required
@csrf_exempt
def device_review(req):

	returnmsg=cimc_device_req(req)
	if returnmsg!=None:
		return HttpResponse(returnmsg)
	device=[]
	devicebind=[]
	device_review=[]
	bind_review=[]
	for i in cimc_device.objects.order_by("-recordtime"):
		username='name'
		userid=i['userid']
		if i['status']==0 or i['status']==1:
			if i['level']==3:
				item=[]
				user_item=cimc_user.objects(userid=userid).first()
				if user_item==None:
					username='noname'
				else:
					username=user_item.username
				item.append(username)
				item.append(i['devicecompany'])
				item.append(i['devicetype'])
				item.append(i['chaintype'])	
				#if 'serialnumber' in i:
				#	serial_list=i['serialnumber']
				#else:
				#	serial_list=['no','serialnumber']
				#serial_split=''			
				#for j,serial_item in enumerate(serial_list):
				#	if j!=(len(serial_list)-1):
				#		serial_split=serial_split+serial_item+'/'
				#	else:
				#		serial_split=serial_split+serial_item
				#item.append(serial_split)
				uploadtime=float(i['recordtime'])
				item.append(transfer_time(uploadtime))
				item.append(i['deviceid'])
				devicebind.append(item)
			elif i['level']==2:
				item=[]
				user_item=cimc_user.objects(userid=userid).first()
				if user_item==None:
					username='noname'
				else:
#					for user_item in col_user.find({'userid':userid}):
					username=user_item.username
				item.append(username)
				item.append(i['devicecompany'])
				item.append(i['devicetype'])
				item.append(i['chaintype'])
				uploadtime=float(i['recordtime'])
				item.append(transfer_time(uploadtime))
				item.append(i['deviceid'])
				device.append(item)
		elif i['level'] != 1:
			item=[]
			user_item=cimc_user.objects(userid=userid).first()
			if user_item==None:
				username='noname'
			else:
			#for user_item in col_user.find({'userid':userid}):
				username=user_item.username
			item.append(username)
			if i['level']==3:
				item.append('个人用户')
				item.append(i['devicecompany'])
				item.append(i['devicetype'])
				item.append(i['chaintype'])
				#serial_list=i['serialnumber']
				if 'serialnumber' in i:
					serial_list=i['serialnumber']
				else:
					serial_list=['no','serialnumber']
				serial_split=''			
				for j,serial_item in enumerate(serial_list):
					if j!=(len(serial_list)-1):
						serial_split=serial_split+serial_item+'/'
					else:
						serial_split=serial_split+serial_item
				item.append(serial_split)
				#item.append(serial_list)
				uploadtime=float(i['recordtime'])
				item.append(transfer_time(uploadtime))
				if i['status']==2:
					item.append('审核通过')
				else:
					item.append('审核未通过')
				item.append(i['deviceid'])
				bind_review.append(item)
			else:
				item.append('设备厂商')
				item.append(i['devicecompany'])
				item.append(i['devicetype'])
				item.append(i['chaintype'])
				uploadtime=float(i['recordtime'])
				item.append(transfer_time(uploadtime))
				if i['status']==2:
					item.append('审核通过')
				else:
					item.append('审核未通过')
				item.append(i['deviceid'])
				device_review.append(item)
	limit=10

	page=req.GET.get('page','')
	if page == '':
		page = 1
	table=req.GET.get('table','')
	if table == '':
		table = 1
	selectItemList=[device,devicebind,device_review,bind_review]
	index=int(table)-1
	count=len(selectItemList)
	
	resultItem,p_pages=get_page_msg(limit,selectItemList,index,count,page)

	return render_to_response('device-review.html',{'device':resultItem[0],'p_pages_device':p_pages[0],'device_bind':resultItem[1],'p_pages_device_bind':p_pages[1],'device_review':resultItem[2],'p_pages_device_review':p_pages[2],'bind_review':resultItem[3],'p_pages_bind_review':p_pages[3]},context_instance=RequestContext(req,processors=[custom_proc]))

