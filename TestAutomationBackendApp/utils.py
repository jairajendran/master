import secrets
import string
# from django.core.mail import EmailMessage
from django.core.mail.message import EmailMessage
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from TestAutomationProject.settings import EMAIL_HOST_USER
import base64;
import datetime;

class Utils(object):
    @staticmethod
    def success_response(data, code=status.HTTP_200_OK):
        response_data = {
            "data": data,
            "message": "SUCCESS",
            "code": code
        }
        return Response(response_data)
    @staticmethod
    def failure_response(data, code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        response_data = {
            "data": data,
            "message": "FAILURE",
            "code": code
        }
        return Response(response_data)
    @staticmethod
    def password_reset_mail(to_list, context):
        subject="Password Reset"
        msg_html = render_to_string("email.html", context)
        msg = EmailMessage(subject=subject, body=msg_html, from_email=EMAIL_HOST_USER, to=to_list)
        msg.content_subtype = "html"  # Main content is now text/html
        return msg.send()
    @staticmethod
    def generate_random_password(length=10):
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                       for i in range(length))
    @staticmethod
    def generate_token():
        return secrets.token_urlsafe()

    @staticmethod
    def Encryption(password):
        pass_encode = password.encode("ascii")
        base64_bytes = base64.b64encode(pass_encode)
        base64_string = base64_bytes.decode("ascii")
        return base64_string

    @staticmethod
    def datetime_validator(input):
        return datetime.datetime.strptime(input,'%d-%m-%Y %I:%M:%S %p')

    @staticmethod
    def send_note_to_release_device(to_email, cc_mail, context):
        # print(to_email)
        subject = 'Request For Releasing A Device'
        sender_note_html = render_to_string('send_note_mail.html', context)
        msg = EmailMessage(subject=subject, body=sender_note_html, from_email=EMAIL_HOST_USER, to=[to_email],cc=[cc_mail])
        # msg = EmailMessage(subject=subject, body=sender_note_html, from_email=EMAIL_HOST_USER, to=[to_email])
        msg.content_subtype = "html"  # Main content is now text/html
        return msg.send()

    @staticmethod
    def User_Does_not_Exists(data, code=status.HTTP_404_NOT_FOUND):
        response_data = {
            "data": data,
            "message": "Failure",
            "code": code
        }
        return Response(response_data)

    @staticmethod
    def executionResponse(deviceData, applicationData, userData, executionDate):
        response_data = {
            "devices": deviceData,
            "executionStatus": 1,
            "executionDate": executionDate,
            "application": applicationData,
            "user": userData
        }
        return Response(response_data)