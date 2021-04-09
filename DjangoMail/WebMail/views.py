# Django lib
from django.shortcuts import render
from django.http import JsonResponse
from django_redis import get_redis_connection
from django.utils import timezone
from django.core import paginator
from django.conf import settings   # = DjangoMail?
import logging

# Django Restful Framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets

# Other app files
from WebMail import models
from WebMail import customSerializers
from WebMail import filters
from WebMail import paginations

# Standard libs
import json
# Create your views here.

# Set log file
logger = logging.getLogger("django")


# Authenticate whether user logined in
# Used by method_decorator
def LoginAuthenticate(function):
    def authenticate(request, *args, **kwargs):
        if request.COOKIES.get('sessionid', None):
            if request.session.get("isLogin", None):
                return function(request, *args, **kwargs)
            else:
                return JsonResponse({"message": "您尚未登录，请先登录", "status": 404})
        else:
            return JsonResponse({"message": "无登录信息，请先登录", "status": 404})
    return authenticate


# Authenticate whether admin logined in
# Used by method_decorator
def AdminAuthenticate(function):
    def authenticate(request, *args, **kwargs):
        if request.COOKIES.get('sessionid', None):
            authority = request.session.get("authorityValue", None)
            if authority == "1" or authority == "2":
                return function(request, *args, **kwargs)
            else:
                return JsonResponse({"message": "您的权限不足，无法访问此页面", "status": 404})
        else:
            return JsonResponse({"message": "无登录信息，请先登录", "status": 404})
    return authenticate


# Authenticate whether super admin logined in
# Used by method_decorator
def SuperAdminAuthenticate(function):
    def authenticate(request, *args, **kwargs):
        if request.COOKIES.get('sessionid', None):
            authority = request.session.get("authorityValue", None)
            if authority == "2":
                return function(request, *args, **kwargs)
            else:
                return JsonResponse({"message": "您的权限不足，无法访问此页面", "status": 404})
        else:
            return JsonResponse({"message": "无登录信息，请先登录", "status": 404})
    return authenticate

# Function: log in

# Function: log out

# Function: help doc

# Function: 

# Function: show config
def ShowConfig(request):
    if request.session.get('isLogin', None):
        auth = request.session.get('authorityValue', None)
        if auth != '2':
            return JsonResponse({
                "message": "您的权限不足",
                "status": 404
            })
        elif request.method == "GET":
            configJson = settings.mailSystemServer.config_show()
            if configJson == -1:
                return JsonResponse({
                    "message": "配置文件读取失败",
                    "status": 404
                })    

            return JsonResponse({
                "data": json.dumps(configJson),
                "message": "成功",
                "status": 200
            })
        else:
            return JsonResponse({
                "message": "请求方式未注册",
                "status": 404
            })
    else: # 
        return JsonResponse({
            "message": "您尚未登录",
            "status": 404
        })

# Function: modify config
def ModifyConfig(request):
    if request.session.get('isLogin', None):
        auth = request.session.get('authorityValue', None)
        if auth != '2':
            return JsonResponse({
                "message": "您未登录或权限不足",
                "status": 404
            })
        elif request.method == 'POST':  # 判断合法性
            configJson = request.POST.get('configJson', None)
            if configJson != None:
                updatedConfig = settings.mailSystemServer.config_modify(json.loads(configJson))
                return JsonResponse({
                    "data": json.dumps(updatedConfig)
                    "message": "修改成功",
                    "status": 200
                })
            else:
                pass
        else:
            return JsonResponse({
                "message": "请求方式未注册",
                "status": 404
            })
            
    else:
        return JsonResponse({
            "message": "您尚未登录",
            "status": 404
        })


# Function: reset config

def ResetConfig(request):
    if request.session.get('isLogin', None):
        auth = request.session.get('authorityValue', None)
        if auth != '2':
            return JsonResponse({
                "message": "您未登录或权限不足",
                "status": 404
            })
        elif request.method == 'GET':
            return JsonResponse({
                "data": json.dumps(settings.mailSystemServer.config_default()),
                "message": "成功",
                "status": 200
            })
        else:
            return JsonResponse({
                "message": "请求方式未注册",
                "status": 404
            })
    else:
        return JsonResponse({
            "message": "您尚未登录",
            "status": 404
        })

# Function: control pop3
def ControlPop3Server(request):
    if request.session.get('isLogin', None):
        auth = request.session.get('authorityValue', None)
        if auth != "2":
            return JsonResponse({
                "message": "您未登录或权限不足",
                "status": 404
                })
    elif request.method == "POST":
        method = request.POST.get("method", None)

        if method == "start":
            settings.mailSystemServer.pop3.start()
        elif method == "restart":
            settings.mailSystemServer.pop3.restart()
        elif method == "stop":
            settings.mailSystemServer.pop3.stop()
        else:
            return JsonResponse({
                "message": "命令错误或未填写命令",
                "status": 404
                })
        return JsonResponse({
            "message": method+"successfully!",
            "status": 200
            })
    else:
        return JsonResponse({
            "message": "请求方式未注册",
            "status": 404
            })


# Function: send mails
def SendMails(request):
    if request.session.get('isLogin', None):
        return JsonResponse({"message": "你已经登录", "status": 404})
    elif request.method == "POST":
        receivers = request.POST.get("receviers", None)
        subject = request.POST.get("subject", None)
        copys = request.POST.get("copys", None)
        content = request.POST.get("content", None)

        userNo = request.session.get("userNo", None)

        if receivers and subject and copys and content:
            receiverList = json.loads(receivers)

            try:
                # Search for sender
                sender = models.Users.objects.filter(userNo=int(userNo))
                if not sender.exist():
                    return JsonResponse({
                        "message": "当前登录用户不合法！",
                        "status": 404
                    })

                sender = sender.first()

                # Create new mails
                newMailList = []
                for receiver in receiverList:
                    newMailInfo = models.Mails.objects.create(
                        receivers=receiver,
                        sender=sender.mailAddress,
                        subject=subject,
                        isRead=False,
                        isServed=0,
                        content=content,
                        userNo=sender
                    )
                    newMailList.append(newMailInfo)

            except Exception as e:
                logging.error('str(Exception):\t', str(Exception))
                logging.error('str(e):\t\t', str(e))
                logging.error('repr(e):\t', repr(e))
                logging.error('########################################################')
                return JsonResponse({"message": "数据库出错，邮件发送失败", "status": 404})
        else:
            return JsonResponse({
                "message": "表单未填写完整",
                "status": 404
            })

        return JsonResponse({
            "message": "发送完成",
            "status": 200
            })
    else:
        return JsonResponse({
            "message": "请求方式未注册",
            "status": 404
            })

# Function: config


# Classes inherited from ModelViewSet which can generate RESTFUL URI
# @method_decorator(LoginAuthenticate, name='dispatch')
class UsersViewSet(viewsets.ModelViewSet):
    queryset = models.Users.objects.all()
    serializer_class = customSerializers.UsersSerializer


# @method_decorator(LoginAuthenticate, name='dispatch')
class MailsViewSet(viewsets.ModelViewSet):
    queryset = models.Mails.objects.all()
    serializer_class = customSerializers.MailsSerializer


# @method_decorator(LoginAuthenticate, name='dispatch')
class ContactsViewSet(viewsets.ModelViewSet):
    queryset = models.Contacts.objects.all()
    serializer_class = customSerializers.ContactsSerializer


# @method_decorator(LoginAuthenticate, name='dispatch')
class AttachmentsViewSet(viewsets.ModelViewSet):
    queryset = models.Attachments.objects.all()
    serializer_class = customSerializers.AttachmentsSerializer


# 为ModelViewSet添加过滤器分页器的样例
# # @method_decorator(LoginAuthenticate, name='dispatch')
# class CaseViewSet(viewsets.ModelViewSet):
#     queryset = models.CaseData.objects.all()
#     serializer_class = customSerializers.CaseDataSerializer
#     pagination_class = paginations.MyFormatResultsSetPagination
#     filter_backends = (OrderingFilter, DjangoFilterBackend)
#     filter_class = filters.CaseFilter
#     ordering_fields = ('caseName', 'initTotal', 'initTotalInfected', 'cityNumber', 'roadNumber',)
#     ordering = ('caseId',)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if (instance):
#             models.AccountInformation.objects.filter(userId=instance.userId.userId).update(caseNumber=F("caseNumber") - 1)
#         return super(CaseViewSet, self).destroy(request, *args, **kwargs)
