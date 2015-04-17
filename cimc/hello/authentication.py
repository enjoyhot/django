#! /usr/bin/env python
#coding=utf-8
from django.shortcuts import render_to_response,RequestContext
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from mongoengine import *
from mongoengine.django.auth import User
from cimc2.settings import DBname,DBhost,DBusername,DBpassword
#connect(DBname,host=DBhost,username=DBusername,password=DBpassword)
#connect('cimc',host='127.0.0.1',username='cimc',password='lab501')
connect('cimc',host='127.0.0.1')
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
				# two methods
				user = authenticate(username=value[0], password=value[1])
				if user is not None:
					user.backend='mongoengine.django.auth.MongoEngineBackend'
					login(req,user)
					admin_name = value[0]
					return HttpResponseRedirect('/cimc/index.html')
				#user=User.objects.get(username=value[0])
				#if user is not None:
				#	if user.check_password(value[1]):
				#		user.backend='mongoengine.django.auth.MongoEngineBackend'
				#		login(req,user)
				#		return HttpResponseRedirect('/cimc/index.html')
				
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

def register():
    import os
    from mongoengine.queryset import DoesNotExist
    valid_user_file = os.getcwd() + "/cimc2/valid_user"
    try:
        with open(valid_user_file,'r') as f:
            for line in f:
                value = line.split('%')
		user = None
		try:
	            user=User.objects.get(username=value[0])
        	except DoesNotExist:                    
                    User.create_user(username=value[0],password=value[1])   
    except IOError:
	#User.create_user(username='cimc3',password='123')	
        pass
