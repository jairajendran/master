from django.contrib.auth.models import AbstractUser
from djongo import models
from TestAutomationProject import settings    

class User(AbstractUser):
    roles_choices = (
        ("User", "User"),
        ("Admin", "Admin")
    )
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)
    email = models.EmailField()
    roles = models.CharField(max_length=20, choices=roles_choices)

class Location(models.Model):
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)
    class Meta:
        abstract = True

class DeviceUser(models.Model):
    deviceId = models.CharField(max_length=23)
    email = models.EmailField()
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    ExecutionStatus = models.BooleanField(default=False)
    requestUser = models.IntegerField(default=0)

class Device(models.Model):
    _class = models.CharField(max_length=100)
    _id = models.CharField(max_length=23)
    communicationPort = models.CharField(max_length=23)
    connectionType: models.BigIntegerField(10)
    deviceState = models.CharField(max_length=23)
    deviceStatus= models.BooleanField(default=False)
    emailId = models.CharField(max_length=60)
    imagePort = models.CharField(max_length=23)
    imei = models.CharField(max_length=23)
    ipAddress = models.CharField(max_length=23)
    location = models.EmbeddedField(model_container=Location, default=None)
    macAddress = models.CharField(max_length=23)
    mdn = models.CharField(max_length=23)
    modelColor = models.NullBooleanField
    modelName = models.CharField(max_length=23)
    modelNumber = models.CharField(max_length=23)
    oem = models.CharField(max_length=23)
    oemColor = models.CharField(max_length=23)
    os = models.CharField(max_length=23)
    osVersion = models.CharField(max_length=23)
    serialNumber = models.CharField(max_length=23)
    team = models.CharField(max_length=23)
    user = models.ForeignKey(DeviceUser,on_delete=models.SET_NULL,null=True,blank=True)
    videoStreamingPort = models.CharField(max_length=23)

class Application(models.Model):
    id = models.AutoField(primary_key=True)
    appName = models.CharField(max_length=23)
    totalDevices = models.BigIntegerField(10)
    totalScenarios = models.BigIntegerField(10)
    activeStatus = models.BooleanField(default=True)
    preConditionStatus = models.BigIntegerField(10)
    objectRunStatus = models.BigIntegerField(10)

class TestScenarios(models.Model):
    id = models.AutoField(primary_key=True)
    scenarioName = models.CharField(max_length=50)
    scenarioDescription = models.CharField(max_length=100)
    activeStatus = models.BooleanField(default=True)
    _id = models.ForeignKey(Application, related_name='testscenarios', on_delete=models.CASCADE)

class TestData(models.Model):
    id = models.AutoField(primary_key=True)
    testDataName = models.CharField(max_length=50)
    testDataDescription = models.CharField(max_length=50)
    testDataStatus = models.BooleanField(default=True)
    _id = models.ForeignKey(TestScenarios, related_name='testdata', on_delete=models.CASCADE)

class ExecutionData(models.Model):
    userEmail = models.EmailField()
    devices = models.TextField(blank=False)
    applicationId = models.BigIntegerField(10)
    executionStatus = models.IntegerField(10)
    executionDate = models.CharField(max_length=50)
