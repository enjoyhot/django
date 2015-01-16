from django.db import models
from mongoengine import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
import time
connect('cimc_user',host='127.0.0.1')

# Create your models here.
class cimc_message(Document):
	msg_from=StringField(required=True)
	to=IntField(required=True)
	msg_type=StringField(required=True)
	time=IntField(required=True)
	status=IntField(required=True)
	result=IntField(required=True)
	devicetype=StringField(required=False)
	devicenumber=StringField(required=False)
	midwareid=IntField(required=False)
	def insert(self):
		self.save()
class cimc_user(Document):
	userid=IntField(required=True)
	password=StringField(required=True)
	username=StringField(required=True)
	email=StringField(required=True)
	regtime=IntField(required=True)
	status=IntField(required=True)
	recordname=StringField(required=True)
	recordcode=StringField(required=True)
	recordtelphone=IntField(required=True)
	recordcompany=StringField(required=True)
	recordaddress=StringField(required=True)
	recordtype=IntField(required=True)
	def insert(self):
		self.save()
class locate_class(Document):
	longtitude=IntField(required=True)
	latitude=IntField(required=True)
class cimc_device(Document):
	deviceid=IntField(required=True)
	userid=IntField(required=True)
	devicecompany=StringField(required=True)
	count=IntField(required=False)
	pid=IntField(required=True)
	level=IntField(required=True)
	status=IntField(required=True)
	recordtime=IntField(required=True,default=int(time.time()))
	chaintype=ListField(StringField(required=False),required=False)
	devicetype=StringField(required=False)
	devicenumber=StringField(required=False)
	serialnumber=ListField(StringField(required=False),required=False)
	location=DictField(required=False)
	updatetime=IntField(required=False)
	def insert(self):
		self.save()


class cimc_midware(Document):
	middlewarename=StringField(required=True)
	devicecompany=StringField(required=True)
	devicetype=StringField(required=True)
	userid=IntField(required=True)
	midwareversion=StringField(required=True)
	midwaremsg=StringField(required=True)
	size=IntField(required=True)
	path=StringField(required=True)
	uploadtime=IntField(required=True)
	md5=StringField(required=True)
	status=IntField(required=True)
	midwareid=IntField(required=True)

	urlapi=StringField(required=True)
	logpath=StringField(required=True)
	totalcount=IntField(required=True)
	successcount=IntField(required=True)
	def insert(self):
		self.save()

#function for cimc_message
def cimc_message_update(**msg_dic):
	if msg_dic['msg_type']=='2':
		cimc_message.objects.get_or_create(msg_from='admin',to=msg_dic['to'],msg_type=msg_dic['msg_type'],devicetype=msg_dic['devicetype'],status=0,defaults=msg_dic)
	elif msg_dic['msg_type']=='4':
		cimc_message.objects.get_or_create(msg_from='admin',to=msg_dic['to'],msg_type=msg_dic['msg_type'],midwareid=msg_dic['midwareid'],status=0,defaults=msg_dic)
	elif msg_dic['msg_type']=='3' or msg_dic['msg_type']==5:
		cimc_message.objects.get_or_create(msg_from='admin',to=msg_dic['to'],msg_type=msg_dic['msg_type'],devicenumber=msg_dic['devicenumber'],status=0,defaults=msg_dic)
	else:
		cimc_message.objects.get_or_create(msg_from='admin',to=msg_dic['to'],msg_type=msg_dic['msg_type'],status=0,defaults=msg_dic)
def cimc_message_delete(**msg_dic):
	if msg_dic['msg_type']=='2':
		cimc_message.objects(to=msg_dic['to'],msg_type=msg_dic['msg_type'],devicetype=msg_dic['devicetype']).delete()
	elif msg_dic['msg_type']=='3':
		cimc_message.objects(to=msg_dic['to'],msg_type=msg_dic['msg_type'],devicenumber=msg_dic['devicenumber']).delete()
	elif msg_dic['msg_type']=='4':
		cimc_message.objects(to=msg_dic['to'],msg_type=msg_dic['msg_type'],midwareid=msg_dic['midwareid']).delete()
	else:
		cimc_message.objects(to=msg_dic['to'],msg_type=msg_dic['msg_type']).delete()

#update fun for cimc_user
def cimc_user_update(userid,status):
	cimc_user.objects(userid=userid).update_one(upsert=False,set__status=status)
#update fun for cimc_midware
def cimc_midware_update(userid,status):
	cimc_midware.objects(userid=userid).update_one(upsert=False,set__status=status)
#update fun for cimc_device
def cimc_device_id(deviceid,*serialnumber):
	cimc_device.objects(deviceid=deviceid,level=3).update_one(upsert=False,set__serialnumber=serialnumber)
	return True

def cimc_device_update(deviceid,level,status):
	cimc_device.objects(deviceid=deviceid,level=level).update_one(upsert=False,set__status=status)
#	return True
	


