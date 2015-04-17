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
from hello.paging import get_page_msg

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

	page=req.GET.get('page','')
	if page == '':
		page = 1
	table=req.GET.get('table','')
	if table == '':
		table = 1
	selectItemList=[user,user_review]
	index=int(table)-1
	count=len(selectItemList)
	
	resultItem,p_pages=get_page_msg(limit,selectItemList,index,count,page)
	# custom_proc function is for global variable
	return render_to_response('user-review.html',{'user':resultItem[0],'p_pages_user':p_pages[0],'user_review':resultItem[1],'p_pages_user_review':p_pages[1]},context_instance=RequestContext(req,processors=[custom_proc]))
