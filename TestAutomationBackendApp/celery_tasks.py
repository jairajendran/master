import django 
import sender as sender 
import requests 
from TestAutomationProject import settings 
from celery import Celery 
from celery.schedules import crontab 
import os 
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1') 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TestAutomationProject.settings") 
import django 
django.setup() 
# Create celery instance 
app = Celery('TestAutomationBackendApp', broker=settings.REDIS_URL) 
 
# get broker + backend settings from main settings file 
app.config_from_object('django.conf:settings', namespace="CELERY") 
 
# discover tasks in all applications, must be in installed Apps 
app.autodiscover_tasks() 
@app.on_after_configure.connect 
def setup_periodic_tasks(sender, **kwargs): 
    sender.add_periodic_task(crontab(minute=0, hour=0), device_auto_release_celery.s(), name="Release the Device at every midnight 12:00am") 



 
@app.task 
def device_auto_release_celery(): 
    url='http://127.0.0.1:8000/api/deviceautorelease/'
    requests.post(url)
# Here is the logic api call from views as per the requests. 
    print('Device Released') 