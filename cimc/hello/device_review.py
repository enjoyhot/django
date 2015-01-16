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
			#if 'serialnumber' in i:
			#	serial_list=i['serialnumber']
			#else:
			#	serial_list=['no','serialnumber']
			#if i['level']==3:
			#	item.append(serial_list)
			#else:
			#	item.append('XXXXXXXXX')
			#uploadtime=float(i['recordtime'])
			#item.append(transfer_time(uploadtime))
			#if i['status']==2:
			#	item.append('审核通过')
			#else:
			#	item.append('审核未通过')
			#item.append(i['deviceid'])
				device_review.append(item)
	limit=10
	page_device=Paginator(device,limit)
	page_device_bind=Paginator(devicebind,limit)
	page_device_review=Paginator(device_review,limit)
	page_bind_review=Paginator(bind_review,limit)
	page=req.GET.get('page')
	table=req.GET.get('table','none')
	try:
		if table=='1':
			device=page_device.page(page)
		else:
			device=page_device.page(1)
	except PageNotAnInteger:
		device=page_device.page(1)
	except EmptyPage:
		device=page_device.page(page_device.num_pages)
	try:
		if table=='2':
			devicebind=page_device_bind.page(page)
		else:
			devicebind=page_device_bind.page(1)
	except PageNotAnInteger:
		devicebind=page_device_bind.page(1)
	except EmptyPage:
		devicebind=page_device_bind.page(page_device_bind.num_pages)

	try:
		if table=='3':
			device_review=page_device_review.page(page)
		else:
			device_review=page_device_review.page(1)
	except PageNotAnInteger:
		device_review=page_device_review.page(1)
	except EmptyPage:
		device_review=page_device_review.page(page_device_review.num_pages)
	try:
		if table=='4':
			bind_review=page_bind_review.page(page)
		else:
			bind_review=page_bind_review.page(1)
	except PageNotAnInteger:
		bind_review=page_bind_review.page(1)
	except EmptyPage:
		bind_reivew=page_bind_review.page(page__bind_review.num_pages)
	return render_to_response('device-review.html',{'device':device,'device_bind':devicebind,'device_review':device_review,'bind_review':bind_review},context_instance=RequestContext(req))

