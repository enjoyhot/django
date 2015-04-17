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
@csrf_protect
def middleware_review(req):
	
	cimc_midware_req(req)

	midware=[]
	midware_test=[]
	midware_review=[]
	for i in cimc_midware.objects.order_by("-uploadtime"):
		if i['status']==0 or i['status']==1:
			item=[]
			useritem=cimc_user.objects(userid=int(float(i['userid']))).first()
			item.append(useritem['username'])
			item.append(i['devicecompany'])
			item.append(i['midwareversion'])
			item.append(i['devicetype'])
			uploadtime=float(i['uploadtime'])
			item.append(transfer_time(uploadtime))
			item.append(i['midwareid'])
			if i['status']==0:
				midware.append(item)
			else:
				midware_test.append(item)
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

	page=req.GET.get('page','')
	if page == '':
		page = 1
	table=req.GET.get('table','')
	if table == '':
		table = 1
	selectItemList=[midware,midware_review,midware_test]
	index=int(table)-1
	count=len(selectItemList)
	
	resultItem,p_pages=get_page_msg(limit,selectItemList,index,count,page)

	return render_to_response('middleware-review.html',{'midware':resultItem[0],'p_pages_midware':p_pages[0],'midware_test':resultItem[2],'p_pages_midware_test':p_pages[2],'midware_review':resultItem[1],'p_pages_midware_review':p_pages[1]},context_instance=RequestContext(req,processors=[custom_proc]))
