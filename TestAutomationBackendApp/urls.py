from django.conf.urls import url
from django.urls import path, include
 
from TestAutomationBackendApp import views
from rest_framework import routers


from django.views.generic.base import TemplateView

 
urlpatterns = [
    # url(r'^apitest/$',views.TestApi.CalcTest), # for REST API test
    path('signup/',views.SignupView.as_view(),name='signup-view'),
    path('login/',views.LoginView.as_view(),name='login-view'),
    path('forgot-password/', views.ForgotPassword.as_view(), name='forgotpassword-view'),
    path('change-password/', views.ChangePassword.as_view(), name='changepassword-view'),
    path('devicelist/', views.DeviceList.as_view(), name='device_list'),
    path('devicereserve/',views.DeviceReserve.as_view(),name="device_reserve"),
    path('devicerelease/',views.DeviceRelease.as_view(),name='devicerelease'),
    path('send-note/', views.SendNoteToReleaseDevice.as_view(), name='send-note-view'),
    path('deviceStatus/', views.Device_Status.as_view(), name='device-status-view'),
    path('device_reserved_list/', views.DeviceReserveList.as_view(), name='device_reserved_list'),

    #Auto release of device url
    path('deviceautorelease/', views.DeviceAutoRelease.as_view(), name='deviceauto'),

    # Urls for adding,getting,updataing and deleting an application
    path('add_application/', views.addApplication.as_view(), name='add-application'),
    path('application_list/', views.getApplicationList.as_view(), name='application_list'),
    path('application_detail/<int:pk>/', views.getApplicationDetail.as_view(), name='list_detail'),


    # Urls for adding,getting,updataing and deleting an scenario
    path('add_scenarios/', views.addTestScenarios.as_view(), name='add_scenarios'),
    path('scenarios_list/', views.getTestScenariosList.as_view(), name='scenarios_list'),
    path('scenarios_detail/<int:pk>/', views.getTestScenariosDetail.as_view(), name='scenarios_detail'),

    # Urls for adding,getting,updataing and deleting an test_data
    path('add_testdata/', views.addTestData.as_view(), name='add_testdata'),
    path('testdata_list/', views.getTestDataList.as_view(), name='testdata_list'),
    path('testdata_detail/<int:pk>/', views.getTestDataDetail.as_view(), name='testdata_detail'),

    #Url for reserve devices list
    path('device_reserve_lis_by_user/',views.DeviceReserveListByUser.as_view(), name='device_reserve_lis_by_user'),

    #Url for getting the Execution Test Data on Running the test cases with the selected reserved devices
    path('execution_json_data/', views.ExecutionJsonData.as_view(), name='Execution_Json_Data'),

]