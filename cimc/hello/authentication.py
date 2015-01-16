
from django.shortcuts import render_to_response,RequestContext
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from mongoengine import *
from mongoengine.django.auth import User
@csrf_exempt
def cimc_login(req):
	from mongoengine.queryset import DoesNotExist
	#from mongoengine.django.auth import User
	#User.create_user(username='cimc',password='123')	
	if req.method=='POST':
		#get the username and the password, then compare to thoes from the table user of databases cimc
		pass_con=req.POST.get('content','')
		if pass_con != '':
			value=pass_con.split(',')
			try:
				user=User.objects.get(username=value[0])
				if user.check_password(value[1]):
					user.backend='mongoengine.django.auth.MongoEngineBackend'
					login(req,user)
					#print 'return'
					return HttpResponseRedirect('/cimc/index.html')
				else:
					#pass
					password_is_wrong='wrong'
					return render_to_response('login.html',{'password_is_wrong':password_is_wrong})
			except DoesNotExist:
				password_is_wrong='wrong'
				return render_to_response('login.html',{'password_is_wrong':password_is_wrong})
	return render_to_response('login.html',{})
	
def cimc_logout(req):
	logout(req)
	return HttpResponseRedirect('/cimc/login')
