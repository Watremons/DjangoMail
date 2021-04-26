# Django lib
from django.http import JsonResponse
from django_redis import get_redis_connection
from django.utils import timezone
from django.core import paginator
from django.conf import settings   # = DjangoMail?
import logging

# Django Restful Framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import viewsets

# Other app files
from WebMail import models
from WebMail import customSerializers
from WebMail import filters
from WebMail import paginations

# Standard libs
import json

# Import server
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from MailSystem.server import Server
mailSystemServer = Server()

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


# Function: Request check
def Check(request, authLevel: list, methodType: str) -> dict:
    if request.session.get('isLogin', None):
        auth = request.session.get('authorityValue', None)
        if auth not in authLevel:
            return {"result": False, "message": "您权限不足"}
        if request.method != methodType:
            return {"result": False, "message": "请求方式未注册"}
        else:
            return {"result": True, "message": "通过验证"}
    else:
        return {"result": False, "message": "您尚未登录"}


# Function: Sign up
def Signup(request):
    if request.session.get('isLogin',None):
        # 登录状态不允许注册。
        return JsonResponse({"message": "登录状态，无法注册", "status": 404})
    elif request.method == "POST":
        
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        sameNameUser = models.Users.objects.filter(userName=username)
        if username and password:  # 获取数据    
            if sameNameUser:  # 用户名唯一
                return JsonResponse({"message": "用户名已经存在，请使用其他用户名，或直接登录！", "status": 404})
            else:
            

                newUser = models.Users.objects.create(
                    userName=username,
                    userPassword=password,
                    authorityValue=0,
                    userState=1
                )
                # logger.debug(json.dumps(newUser))

                return JsonResponse({"message": "注册成功", "status": 200})
            # except Exception as e:
            #     logging.error('str(Exception):\t', str(Exception))
            #     logging.error('str(e):\t\t', str(e))
            #     logging.error('repr(e):\t', repr(e))
            #     logging.error('e.message:\t', e.args)
            #     logging.error('########################################################')

            #     return JsonResponse({"message": "数据库出错，注册失败", "status": 200})
        else:
            return JsonResponse({"message": "注册表单填写不完整", "status": 404})
    else:
        return JsonResponse({"message": "请求方式未注册", "status": 404})

                
# Function: log in
def Signin(request):
    # 若已经登录，直接进入已登录账号
    if request.session.get('isLogin', None):
        return JsonResponse({"message": "你已经登录", "status": 404})
    elif request.method == "POST":
        # 从参数获取userName和password
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:
            try:
                # 获取失败则捕捉错误
                profile = models.Users.objects.filter(userName=username)
                if not profile.exists():
                    return JsonResponse({"message": "该账号不存在", "status": 404})
                profile = profile.first()
                # accountInfo = models.Users.objects.get(userName=profile.userName)

                if (profile.userPassword == password):
                    # 若相同，设置登录状态为True，设置登录id为userId，登录权限为对应权限
                    request.session['isLogin'] = True
                    request.session['userName'] = profile.userName
                    request.session['authorityValue'] = profile.authorityValue
                    response = JsonResponse({
                        "message": "登录成功",
                        "status": 200,
                        "userName": profile.userName,
                        "authorityValue": profile.authorityValue
                        })
                    return response
                else:
                    return JsonResponse({"message": "密码错误", "status": 404})
            except Exception as e:
                logging.error('str(Exception):\t', str(Exception))
                logging.error('str(e):\t\t', str(e))
                logging.error('repr(e):\t', repr(e))
                logging.error('e.message:\t', e.args)
                logging.error('########################################################')
                return JsonResponse({"message": "数据库错误", "status": 404})
        else:
            return JsonResponse({"message": "登录表单填写不完整", "status": 404})
    else:
        return JsonResponse({"message": "请求方式未注册", "status": 404})



# Function: log out
def Logout(request):
    if not request.session.get('isLogin', None):
        # 如果本来就未登录，也就没有登出一说
        return JsonResponse({"message": "未登录，无法登出", "status": 404})
    else:
        request.session.flush()
        response = JsonResponse({"message": "登出成功", "status": 200})
        return response


# Function: Change Password
def ChangePwd(request):
    if not request.session.get('isLogin', None):
        return JsonResponse({"message": "你还未登录", "status": 404})
    elif request.method == "POST":
        # 从参数获取oldPassword和password
        userNo = request.session.get("userNo", None)
        oldPassword = request.POST.get('oldPassword', None)
        newPassword = request.POST.get('newPassword', None)
        if userNo and oldPassword and newPassword:
            try:
                account = models.Users.objects.filter(userNo=userNo)
                if not account.exists():
                    return JsonResponse({"message": "当前账号与浏览器记录不一致", "status": 404})
                account = account.first()
                # 检测账号原密码是否符合
                if account.userPassword == oldPassword:
                    
                    models.Users.objects.filter(userNo=userNo).update(userPassword=newPassword)
                    return JsonResponse({"message": "修改成功", "status": 200})
                else:
                    return JsonResponse({"message": "账号原密码错误", "status": 404})
            except Exception as e:
                logging.error('str(Exception):\t', str(Exception))
                logging.error('str(e):\t\t', str(e))
                logging.error('repr(e):\t', repr(e))
                logging.error('e.message:\t', e.args)
                logging.error('########################################################')
                return JsonResponse({"message": "数据库出错，修改密码失败", "status": 404})
        else:
            return JsonResponse({"message": "修改密码表单填写不完整", "status": 404})
    else:
        return JsonResponse({"message": "请求方式未注册", "status": 404})

# Function: help doc

# Function:


# Function: show config
def ShowConfig(request):
    checkRes = Check(request, [1, 2], 'GET')
    if not Check["result"]:
        return JsonResponse({
            "message": checkRes["message"],
            "status": 404
        })
    else:
        print(settings.TMP)
        configJson = mailSystemServer.ConfigShow()
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


# Function: modify config
def ModifyConfig(request):
    checkRef = Check(request, [1, 2], 'POST')
    if not checkRef["result"]:
        return JsonResponse({
            "message": checkRef["message"],
            "status": 404
        })
    else:  # 判断合法性
        configJson = request.POST.get('configJson', None)
        if configJson != None:
            updatedConfig = mailSystemServer.ConfigModify(json.loads(configJson))
            return JsonResponse({
                "data": json.dumps(updatedConfig),
                "message": "修改成功",
                "status": 200
            })
        else:
            pass


# Function: reset config
def ResetConfig(request):
    checkRef = Check(request, [1, 2], 'POST')
    if not checkRef["result"]:
        return JsonResponse({
            "message": checkRef["message"],
            "status": 404
        })
    else:
        return JsonResponse({
            "data": json.dumps(mailSystemServer.ConfigDefault()),
            "message": "成功",
            "status": 200
        })


# Function: control smtp
def ControlSmtpServer(request):
    checkRes = Check(request, [1, 2], "POST")
    if not checkRes["result"]:
        return JsonResponse({
            "message": checkRes["message"],
            "status": 404
            })
    else:
        method = request.POST.get("method", None)

        if method == "start":
            settings.mailSystemServer.stmp.start()
        elif method == "restart":
            settings.mailSystemServer.stmp.restart()
        elif method == "stop":
            settings.mailSystemServer.stmp.stop()
        else:
            return JsonResponse({
                "message": "命令错误或未填写命令",
                "status": 404
                })
        return JsonResponse({
            "message": method+"successfully!",
            "status": 200
            })


# Function: control pop3
def ControlPop3Server(request):
    checkRes = Check(request, [1, 2], "POST")
    if not checkRes["result"]:
        return JsonResponse({
            "message": checkRes["message"],
            "status": 404
            })
    else:
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


# Function: send mails
def SendMails(request):
    CheckRes = Check(request, [0, 1, 2], "POST")
    if not CheckRes["result"]:
        return JsonResponse({"message": CheckRes["message"], "status": 404})
    else:
        receivers = request.POST.get("receviers", None)
        content = request.POST.get("content", None)

        userNo = request.session.get("userNo", None)

        if receivers and content:
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
                        receiver=receiver,
                        sender=sender.userName,
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


# Function: receive mails
def ReceiveMails(request):
    CheckRes = Check(request, [0, 1, 2], "POST")
    if not CheckRes["result"]:
        return JsonResponse({"message": CheckRes["message"], "status": 404})
    else:
        userNo = request.session.get("userNo", None)
        try:
            # Search for sender
            receiver = models.Users.objects.filter(userNo=int(userNo))
            if not receiver.exist():
                return JsonResponse({
                    "message": "当前登录用户不合法！",
                    "status": 404
                })

            receiver = receiver.first()

            # Create new mails
            notReadMailList = []
            newMails = models.Mails.objects.filter(
                receiver=receiver.userName,
                isRead=False
            ).values()
            notReadMailList.append(newMails)

            # settings.mailSystemServer.pop3.
        except Exception as e:
            logging.error('str(Exception):\t', str(Exception))
            logging.error('str(e):\t\t', str(e))
            logging.error('repr(e):\t', repr(e))
            logging.error('########################################################')
            return JsonResponse({"message": "数据库出错，邮件发送失败", "status": 404})

        return JsonResponse({
            "message": "发送完成",
            "status": 200
            })
# Function: config


# Class: user authority filter
# class UsersView(ListAPIView):
#     queryset = models.Users.objects.all()
#     serializer_class = customSerializers.UsersSerializer
#     filter_class = filters.UserAuthorityFilter
#     pagination_class = paginations.MyFormatResultsSetPagination


# Classes inherited from ModelViewSet which can generate RESTFUL URI
# @method_decorator(LoginAuthenticate, name='dispatch')
class UsersViewSet(viewsets.ModelViewSet):
    queryset = models.Users.objects.all()
    serializer_class = customSerializers.UsersSerializer
    pagination_class = paginations.MyFormatResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['^userName']
    filter_class = filters.UserFilter


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
# @method_decorator(LoginAuthenticate, name='dispatch')
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
