from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse, Http404

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.template.loader import get_template
from rest_framework import status
from rest_framework.views import APIView


from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import User, Application, TestScenarios, TestData
from .utils import Utils
from TestAutomationProject.settings import EMAIL_HOST_USER, EMAIL_BACKEND
from .serializers import UserSerializer, UserDataSerializer, DeviceSerializer, DeviceDetailSerializer, DeviceReserveSerializer, DeviceListSerializer, DeviceUserSerializer, ReservedDataSerializer, ApplicationSerializer, TestdataSerializer, TestScenariosSerializer, ExceutionDeviceDetailSerializer, ExecutionDataSerializer
from .models import Device
import datetime
from .models import DeviceUser, ExecutionData

#create your views here

# class TestApi():
#     @api_view(["GET"])
#     def CalcTest(self):
#             y=str(10*100)
#             return JsonResponse("Result:"+y,safe=False)

class SignupView(APIView):
    def post(self, request):
        try:
            data = request.data
            user = User.objects.filter(email=data['user_email'])
            if not user:
                user_object = User(username=data['user_email'],
                                   first_name=data['user_firstname'],
                                   last_name=data['user_lastname'],
                                   email=data['user_email'],
                                   roles=data['user_role'])
                user_object.save()
                user_object.set_password(data['user_password'])
                user_object.save()
                return Utils.success_response("SIGNUP_SUCCESSFUL")
            else:
                return Utils.failure_response("Already an User")
        except Exception as e:
            return Utils.failure_response("INTERNAL_SERVER_ERROR")

class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            user = authenticate(username=data['user_email'], password=data['user_password'])
            if user:
                response={'firstname':user.first_name,
                          'lastname':user.last_name,
                          'email':user.email,
                          'role':user.roles}
                return Utils.success_response(response)
            else:
                return Utils.failure_response("LOGIN_FAILURE", code=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Utils.failure_response("INTERNAL_SERVER_ERROR")
    
    
class ForgotPassword(APIView):
    def post(self, request):
        try:
            data = request.data
            email = data['user_email']
            # print("email: "+email)
            user = User.objects.filter(email=email)
            if user:
                user= user[0]
                # print("user: "+user)
                username=user.first_name+" "+user.last_name
                password = Utils.generate_random_password()
                encrypted=Utils.Encryption(password)
                user.set_password(encrypted)
                user.save()
                context={
                    'username':username,
                    'password':password
                }
                # The dictionary (context) returned by the Context Processor is merged into the context passed in by you (the user) by Django. A use case for a Context Processor is when you always want to insert certain variables inside your template (for example the location of the user could be a candidate).
                Utils.password_reset_mail([email],context)
                return Utils.success_response("Email Sent Successfully")
            else:
                return Utils.failure_response("Enter Valid Email")
        except Exception as e:
            return Utils.failure_response("INTERNAL_SERVER_ERROR")

class ChangePassword(APIView):
    def post(self, request):
        try:
            data = request.data
            password=data['old_password']
            users=User.objects.filter(username=data['username'])
            users=users[0]
            if users.check_password(password):
                users.set_password(data['new_password'])
                users.save()
                return Utils.success_response("password Changed successfully")
            else:
                return Utils.failure_response("Enter Valid Password")
        except Exception as e:
            return Utils.failure_response("INTERNAL_SERVER_ERROR")

class DeviceList(APIView):
    def get(self, request):
        devices = Device.objects.all()
        device_serializer = DeviceDetailSerializer(devices, many=True)
        return Utils.success_response(device_serializer.data)
    def post(self, request):
        device_data = request.data
        devices = Device.objects.filter(_id=device_data['_id'])
        if not devices:
            device_serializer = DeviceSerializer(data=device_data)
            if device_serializer.is_valid():
                device_serializer.save()
                return JsonResponse(device_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(device_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Utils.failure_response("Device is already registered")

class DeviceReserve(APIView):
    def post(self, request):
        data = request.data
        device_queryset = Device.objects.filter(_id=data['device_id']).first()
        if not device_queryset.user :
            user_queryset = User.objects.filter(email=data['username']).first()
            start_date=Utils.datetime_validator(data['start_date'])
            end_date = Utils.datetime_validator(data['end_date'])
            device_user=DeviceUser(email=user_queryset.email,
                                   first_name=user_queryset.first_name,
                                   last_name=user_queryset.last_name,
                                   start_date=start_date,
                                   end_date=end_date)
            device_user.save()
            s_data = {
                "deviceStatus":False,
                "user": device_user.id
            }
            serialize = DeviceSerializer(device_queryset, data=s_data, partial=True)
            if serialize.is_valid():
                serialize.save()
            return Utils.success_response(serialize.data)
        else:
            return Utils.failure_response("Device is already Reserved")

class DeviceRelease(APIView):
    def post(self,request):
        data=request.data
        device_queryset=Device.objects.filter(_id=data['device_id']).first()
        DeviceUser.objects.filter(id=device_queryset.user.id)[0].delete()
        s_data = {
            "deviceStatus": True,
            "user":None
        }
        serialize = DeviceSerializer(device_queryset, data=s_data, partial=True)
        if serialize.is_valid():
            serialize.save()
            return Utils.success_response(serialize.data)

class SendNoteToReleaseDevice(APIView):
    def post(self, request):
        try:
            data=request.data
            device_user_queryset = DeviceUser.objects.filter(email=data['reserved_user_id']).first()
            user_queryset=User.objects.filter(username=data['username']).first()
            receiver_email = device_user_queryset.email
            to_name = device_user_queryset.first_name +"_"+device_user_queryset.last_name
            from_name = user_queryset.first_name +"_"+user_queryset.last_name
            sender_note = request.data['Sender_Note'],
            cc_mail=data['username']
            if sender_note == '':
                sender_note = 'Request to release the device as the other user wants to use it'
            context = {
                'sender_note': sender_note,
                'to_name': to_name,
                'from_name': from_name
            }
            sent_mail_update = Utils.send_note_to_release_device(receiver_email,cc_mail, context)

            if sent_mail_update == 1:
                device_user_queryset.requestUser=1
                device_user_queryset.save()
                return Utils.success_response("Email Sent Successfully")
            else:
                return Utils.failure_response("Email Sent Was Unsuccessful")
        except Exception as e:
            print('Exception in SendNoteToReleaseDevice()', e)
            return Utils.failure_response("Exception in SendNote_ReleaseDevice()")

class DeviceAutoRelease(APIView):
    def post(self, request):
        end_date = datetime.datetime.now()
        release_queryset = DeviceUser.objects.filter(end_date__lte=end_date)
        for queryset in release_queryset:
            device_queryset = Device.objects.filter(user_id=queryset.id).first()
            device_queryset.deviceStatus = True
            device_queryset.save()
        release_queryset.delete()
        return Utils.success_response("Device Changed")

class Device_Status(APIView):
    def get(self, request):
        devices = Device.objects.all()
        device_serializer = DeviceReserveSerializer(devices, many=True)
        return Utils.success_response(device_serializer.data)

class DeviceReserveList(APIView):
        def get(self,request):
            device = Device.objects.filter(deviceStatus=False)
            reserved_device_data =ReservedDataSerializer(device, many=True).data
            # return Response(data)
            return Utils.success_response(reserved_device_data)

# API for adding an application
class addApplication(APIView):
    def post(self, request):
        application_data = JSONParser().parse(request)
        application_serializer = ApplicationSerializer(data=application_data)
        if application_serializer.is_valid():
            application_serializer.save()
            return Utils.success_response("Application is added successfully..")
        else:
            return JsonResponse(application_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class getApplicationDetail(APIView):
    def get_object(self, pk):
        try:
            return Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            raise Http404
    # API for getting one application
    def get(self, request, pk):
        try:
            application = self.get_object(pk)
            application_serializer = ApplicationSerializer(application)
            return Response(application_serializer.data)
        except Exception as e:
            print('Exception in application details', e)
            return Utils.failure_response("Exception in application details")
    # API for updating one application
    def put(self, request, pk, format=None):
        application = self.get_object(pk)
        serializer = ApplicationSerializer(application, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Utils.success_response("Application is edited successfully..")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # API for deleting an application
    def delete(self, request, pk, format=None):
        application = self.get_object(pk)
        application.delete()
        return Utils.success_response("Application is deleted successfully..")

class getApplicationList(APIView):
    # API for getting list of applications
    def get(self, request):
        applications = Application.objects.all().order_by('appName')
        application_serializer = ApplicationSerializer(applications, many=True)
        return Utils.success_response(application_serializer.data)

# API for adding an Testscenario
class addTestScenarios(APIView):
    def post(self, request):
        test_scenario_data = JSONParser().parse(request)
        test_scenario_serializer = TestScenariosSerializer(data=test_scenario_data)
        if test_scenario_serializer.is_valid():
            test_scenario_serializer.save()
            return Utils.success_response("Test scenario is added successfully")

        return JsonResponse(test_scenario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class getTestScenariosList(APIView):
    # API for getting list of  Testscenario
    def get(self, request):
        testscenarios = TestScenarios.objects.all().order_by('scenarioName')
        testscenarios_serializer = TestScenariosSerializer(testscenarios, many=True)
        return Utils.success_response(testscenarios_serializer.data)


class getTestScenariosDetail(APIView):
    def get_object(self, pk):
        try:
            return TestScenarios.objects.get(pk=pk)
        except Application.DoesNotExist:
            raise Http404

    # API for getting one  Testscenario
    def get(self, request, pk):
        # get details of a single testdata
        testscenario = self.get_object(pk)
        testscenario_serializer = TestScenariosSerializer(testscenario)
        return Response(testscenario_serializer.data)

    # API for updating one Testscenario
    def put(self, request, pk, format=None):
        testscenario = self.get_object(pk)
        serializer = TestScenariosSerializer(testscenario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Utils.success_response("TestScenario is saved successfully")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # API for deleting one Testscenario
    def delete(self, request, pk, format=None):
        testscenarios = self.get_object(pk)
        testscenarios.delete()
        return Utils.success_response("TestScenario is deleted successfully")


# API for adding one Testdata
class addTestData(APIView):
    def post(self, request):
        test_data = JSONParser().parse(request)
        test_data_serializer = TestdataSerializer(data=test_data)
        if test_data_serializer.is_valid():
            test_data_serializer.save()
            return Utils.success_response("TestData is added successfully")

        return JsonResponse(test_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class getTestDataList(APIView):
    # API for getting list of Testdata
    def get(self, request):
        testdata = TestData.objects.all().order_by('testDataName')
        testdata_serializer = TestdataSerializer(testdata, many=True)
        return Utils.success_response(testdata_serializer.data)


class getTestDataDetail(APIView):
    def get_object(self, pk):
        try:
            return TestData.objects.get(pk=pk)
        except Application.DoesNotExist:
            raise Http404

    # API for get details of a single testdata
    def get(self, request, pk):
        testdata = self.get_object(pk)
        testdata_serializer = TestdataSerializer(testdata)
        return Response(testdata_serializer.data)

    # API for updating details of a testdata
    def put(self, request, pk, format=None):
        testdata = self.get_object(pk)
        serializer = TestdataSerializer(testdata, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Utils.success_response("TestData is edited successfully")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # API for deleting a testdata
    def delete(self, request, pk, format=None):
        testdata = self.get_object(pk)
        testdata.delete()
        return Utils.success_response("TestData is deleted successfully")

class DeviceReserveListByUser(APIView):
    def get(self, request):
        email = request.query_params['email']
        reserved_device = Device.objects.filter(deviceStatus=False,user__email=email)
        if not reserved_device:
            return Utils.User_Does_not_Exists("Username doesn't exist,Please enter valid Username")
            print(reserved_device)
        reserved_device_data = DeviceListSerializer(reserved_device, many=True).data
        return Response(reserved_device_data)

class ExecutionJsonData(APIView):
    def post(self, request):
        try:
            data = request.data
            deviceIds = data['device_id']
        
            DeviceUser.objects.filter(deviceId__in=deviceIds).update(ExecutionStatus=True)

            device_user_object = ExecutionData(userEmail=data['userId'],
                                               devices=data['device_id'],
                                               applicationId=data['app_id'],
                                               executionStatus=1,
                                               executionDate=data['executionDate'])
            device_user_object.save()

            DeviceUser.objects.filter(deviceId__in=deviceIds).update(ExecutionStatus=True)
            devices = Device.objects.filter(_id__in=deviceIds)
            device_serializer = ExceutionDeviceDetailSerializer(devices, many=True)

            applicationId = data['app_id']
            application = Application.objects.filter(id=applicationId)
            application_serializer = ApplicationSerializer(application, many=True)

            user_queryset = User.objects.filter(email=data['userId'])
            user_serializer = UserDataSerializer(user_queryset, many=True)

            ExecutionDataJSON = Utils.executionResponse(device_serializer.data, application_serializer.data, user_serializer.data, data['executionDate'])
            return Utils.success_response(ExecutionDataJSON.data)

        except Exception as e:
            print(e)
            return Utils.failure_response("INTERNAL_SERVER_ERROR")