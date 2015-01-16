#coding:utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from hello.forms import UploadFileForm
from hello.models import *
from hello.index import index
from hello.user_review import user_review
from hello.server_info import server_info
from hello.middleware_review import middleware_review
from hello.device_review import device_review
from hello.authentication import *
from hello.solve_req import *
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import time
import hashlib

def kvm_manage(req):
	return render_to_response('kvm-manage.html',{})

