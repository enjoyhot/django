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
@csrf_protect
def middleware_review(req):
	
	cimc_midware_req(req)

	midware=[]
	midware_review=[]
	for i in cimc_midware.objects.order_by("-uploadtime"):
		if i['status']==0:
			item=[]
			useritem=cimc_user.objects(userid=int(float(i['userid']))).first()
			item.append(useritem['username'])
			item.append(i['devicecompany'])
			item.append(i['midwareversion'])
			item.append(i['devicetype'])
			uploadtime=float(i['uploadtime'])
			item.append(transfer_time(uploadtime))
			item.append(i['midwareid'])
			midware.append(item)
		else:
			item=[]
			useritem=cimc_user.objects(userid=int(float(i['userid']))).first()
			item.append(useritem['username'])
			item.append(i['devicecompany'])
			item.append(i['midwareversion'])
			item.append(i['devicetype'])
			uploadtime=float(i['uploadtime'])
			item.append(transfer_time(uploadtime))
			if i['status']==1:
				item.append('审核通过')
			else:
				item.append('审核未通过')
			item.append(i['midwareid'])
			midware_review.append(item)
	limit=10
	page_midware=Paginator(midware,limit)
	page_midware_review=Paginator(midware_review,limit)
	page=req.GET.get('page')
	table=req.GET.get('table','none')
	try:
		if table=='1':
			midware=page_midware.page(page)
		else:
			midware=page_midware.page(1)
	except PageNotAnInteger:
		midware=page_midware.page(1)
	except EmptyPage:
		midware=page_midware.page(page_midware.num_pages)
	try:
		if table=='2':
			midware_review=page_midware_review.page(page)
		else:
			midware_review=page_midware_review.page(1)
	except PageNotAnInteger:
		midware_review=page_midware_review.page(1)
	except EmptyPage:
		midware_review=page_midware_review.page(page_midware_review.num_pages)
	return render_to_response('middleware-review.html',{'midware':midware,'midware_review':midware_review},context_instance=RequestContext(req))
