import json
from rest_framework import serializers
from .models import User, Device, DeviceUser, Application, TestScenarios, TestData, ExecutionData


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceUser
        fields = ('email', 'first_name', 'last_name', 'start_date', 'end_date', 'ExecutionStatus', 'requestUser')

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
        
class DeviceDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    location = serializers.SerializerMethodField()
    class Meta:
        model = Device
        fields = '__all__'
    def get_location(self, obj):
        return json.loads(json.dumps(obj.location,indent=8))

class DeviceReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('deviceStatus',)

class DeviceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceUser
        fields = ('email','first_name','last_name','ExecutionStatus')

class ReservedDataSerializer(serializers.ModelSerializer):
    user = DeviceUserSerializer(required=True)
    class Meta:
        model =Device
        fields =('_id','modelName','deviceStatus','user')

class TestdataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestData
        fields = ('id', 'testDataName', 'testDataDescription', 'testDataStatus', '_id')

class TestScenariosSerializer(serializers.ModelSerializer):
    testdata = TestdataSerializer(read_only=True, many=True)
    class Meta:
        model = TestScenarios
        fields = ('id', 'scenarioName', 'scenarioDescription', 'activeStatus', '_id', 'testdata')

class ApplicationSerializer(serializers.ModelSerializer):
    testscenarios = TestScenariosSerializer(read_only=True, many=True)
    class Meta:
        model = Application
        fields = ('id', 'appName', 'totalDevices', 'totalScenarios', 'activeStatus', 'preConditionStatus',
                  'objectRunStatus', 'testscenarios')

class DeviceListSerializer(serializers.ModelSerializer):
    user = DeviceUserSerializer(required=True)
    class Meta:
        model =Device
        fields =('_id','modelName','deviceStatus','user')

class ExceutionDeviceDetailSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    class Meta:
        model = Device
        fields = '__all__'
    def get_location(self, obj):
        return json.loads(json.dumps(obj.location,indent=8))

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceUser
        fields = ('first_name', 'last_name', 'email')

class ExecutionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutionData
        fields = '__all__'