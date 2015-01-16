#coding:utf-8
import os
import sys
from django.core.wsgi import get_wsgi_application
reload(sys)
sys.setdefaultencoding('utf8')

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","cimc2.settings"
)


#from django.core.handlers.wsgi import WSGIHandler

#application=WSGIHandler()
application=get_wsgi_application()
