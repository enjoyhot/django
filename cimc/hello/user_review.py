#coding:utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from hello.forms import UploadFileForm
from hello.models import *
from hello.index import index
from hello.solve_req import *
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import time
import hashlib
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

@login_required
@csrf_exempt
def user_review(req):
	#the button function
	cimc_user_req(req)

	#display the tables
	user=[]
	user_review=[]
	for i in cimc_user.objects.order_by("-regtime"):
		if i['status']==0 or i['status']==1:
			item=[]
			item.append(i['username'])
			item.append(i['recordname'])
			item.append(i['recordcompany'])
			item.append(i['recordtelphone'])
			item.append(i['recordcode'])
			item.append(i['recordaddress'])
			if int(i['recordtype'])==1:
				item.append('个人用户')
			else:
				item.append('厂商用户')
			item.append(i['userid'])
			user.append(item)
		else:
			item=[]
			item.append(i['username'])
			item.append(i['recordname'])
			item.append(i['recordcompany'])
			item.append(i['recordtelphone'])
			item.append(i['recordcode'])
			regtime=float(i['regtime'])
			item.append(transfer_time(regtime))
			if int(i['recordtype'])==1:
				item.append('个人用户')
			else:
				item.append('厂商用户')
			item.append(i['userid'])
			if i['status']==2:
				item.append('审核通过')
			else:
				item.append('审核未通过')
			user_review.append(item)
	limit=10
	page_user=Paginator(user,limit)
	page_user_review=Paginator(user_review,limit)
	page=req.GET.get('page')
	table=req.GET.get('table','none')
	try:
		if table=='1':
			user=page_user.page(page)
		else:
			user=page_user.page(1)
	except PageNotAnInteger:
		user=page_user.page(1)
	except EmptyPage:
		user=page_user.page(page_user.num_pages)
	try:
		if table=='2':
			user_review=page_user_review.page(page)
		else:
			user_review=page_user_review.page(1)
	except PageNotAnInteger:
		user_review=page_user_review.page(1)
	except EmptyPage:
		user_review=page_user_review.page(page_user_review.num_pages)
	return render_to_response('user-review.html',{'user':user,'user_review':user_review},context_instance=RequestContext(req))
