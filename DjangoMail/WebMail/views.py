# Django lib
from django.http import JsonResponse
from django_redis import get_redis_connection
from django.utils import timezone
from django.core import paginator
from django.forms.models import model_to_dict
from django.db.models import Count
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
import time
from dateutil.relativedelta import relativedelta

# Import server
import os
import sys
import socket
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
    auth = request.POST.get('authorityValue', None)
    if auth:
        if int(auth) not in authLevel:
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
    configJson = request.POST.get('configJson', None)
    if configJson is not None:
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
    return JsonResponse({
        "data": json.dumps(mailSystemServer.ConfigDefault()),
        "message": "成功",
        "status": 200
    })


# Function: get all logs by type
def GetAllLog(request):
    if request.method == "POST":
        logType = request.POST.get('logType', None)
        if logType and (int(logType) == 0 or int(logType) == 1):
            logNames, logPaths, logSizes = mailSystemServer.GetAllLogFile(int(logType))

            logList = []
            for index in range(len(logPaths)):
                f = open(logPaths[index], 'r', encoding='utf-8')
                logContent = f.read()
                logTimestamp = os.path.getatime(logPaths[index])
                f.close()

                logTime = time.strftime(
                    '%Y-%m-%d %H:%M:%S',
                    time.localtime(logTimestamp)
                )
                logList.append({
                    "logName": logNames[index],
                    "logTime": logTime,
                    "logContent": logContent
                    })

            return JsonResponse({
                "data": json.dumps(logList),
                "message": "成功",
                "status": 200
            })
        else:
            return JsonResponse({
                "message": "日志类型参数错误",
                "status": 404
            })
    else:
        return {"status": 404, "message": "请求方式未注册"}


# Function: del logs by index and type
def DelLogsByIdx(request):
    if request.method == "POST":
        logIndexListStr = request.POST.get('logIndexList', None)
        logType = request.POST.get('logType', None)
        if logIndexListStr and logType and (int(logType) == 0 or int(logType) == 1):
            logIndexList = json.loads(logIndexListStr)
            returnList = []
            flag = True
            for index in range(len(logIndexList)):
                if (mailSystemServer.DelLogFile(int(logType), logIndexList[index])):
                    returnList.append(True)
                else:
                    flag = False
                    returnList.append(False)
            if flag:
                return JsonResponse({
                    "data": json.dumps(returnList),
                    "message": "全部成功",
                    "status": 200
                })
            else:
                return JsonResponse({
                    "data": json.dumps(returnList),
                    "message": "存在失败",
                    "status": 201
                })
        else:
            return JsonResponse({
                "message": "日志类型参数错误或表单填写不完整",
                "status": 404
            })
    else:
        return {"status": 404, "message": "请求方式未注册"}


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
            mailSystemServer.smtp.start()
        elif method == "restart":
            mailSystemServer.smtp.restart()
        elif method == "stop":
            mailSystemServer.smtp.stop()
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
            mailSystemServer.pop3.start()
        elif method == "restart":
            mailSystemServer.pop3.restart()
        elif method == "stop":
            mailSystemServer.pop3.stop()
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
def SendMail(request):
    CheckRes = Check(request, [0, 1, 2], "POST")
    if not CheckRes["result"]:
        return JsonResponse({"message": CheckRes["message"], "status": 404})
    else:
        sender = request.POST.get("sender", None)
        receiver = request.POST.get("receiver", None)
        content = request.POST.get("content", None)
        ipAddr = request.POST.get("ipAddr", None)
        subject = request.POST.get("subject", None)

        if sender and receiver and content and ipAddr and subject:

            try:
                # Search for sender
                sender = models.Users.objects.filter(userName=sender)
                if not sender.exists():
                    return JsonResponse({
                        "message": "使用的发送用户不合法！",
                        "status": 404
                    })
                sender = sender.first()
                receiver = models.Users.objects.filter(userName=receiver)
                if not receiver.exists():
                    return JsonResponse({
                        "message": "使用的接收用户不合法！",
                        "status": 404
                    })
                
                receiver = receiver.first()
                # Create new mails
                newMailInfo = models.Mails.objects.create(
                    receiver=receiver.userName,
                    sender=sender.userName,
                    ip=ipAddr,
                    isRead=0,
                    isServed=1,
                    content=content,
                    subject=subject
                )

                return JsonResponse({
                    "message": "发送完成",
                    "sender": sender.userName,
                    "status": 200
                    })

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


# Function: list all unreaded mails
def ListUnreadedMails(request):
    
    checkRes = Check(request, [1, 2, 3], "POST")
    if not checkRes["result"]:
        return JsonResponse({
            "message": checkRes["message"],
            "status": 404
        })
    else:
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        try:
            client = socket.socket()
            pop3_ip_port = ('127.0.0.1', 8110)
            client.connect(pop3_ip_port)
            data = client.recv(1024)
            user_cmd = 'USER ' + username + '\r\n'
            client.send(user_cmd.encode())
            data = client.recv(1024)
            pass_cmd = 'PASS ' + password + '\r\n'
            client.send(pass_cmd.encode())
            data = client.recv(1024)
            list_cmd = 'LIST\r\n'
            client.send(list_cmd.encode())
            data = client.recv(1024).decode()
            # print(data)
            mail_list = data.split('\r\n')[1:-2]
            # print(mail_list)

            mail_json_list = []
            for mail in mail_list:
                
                retr_cmd = 'RETR ' + mail.split()[0] + '\r\n'
                client.send(retr_cmd.encode())
                mail_detail = client.recv(1024).decode()
                mail_item = mail_detail.split('\r\n')[1:-2]

                mail_dict = {}
                mail_dict['mailNo'] = int(mail.split()[0])
                mail_dict['sender'] = mail_item[1].split()[1]
                mail_dict['subject'] = mail_item[3].split()[1]
                mail_dict['isRead'] = 0
                mail_json_list.append(mail_dict)

            return JsonResponse({
                "message": "Return mail list successfully!",
                "status": 200,
                "data": json.dumps(mail_json_list)
            }) 
        except:
            return JsonResponse({
                "message": "Return mail list error!",
                "status": 404
            })


# Function: get single mail for detail by id
def GetMailById(request):
    pass


# Function: get mails by id
# Return mailNo, sender, isRead, subject
def GetAllMailsbyId(request):
    if request.method == "POST":
        userName = request.POST.get("userName", None)
        if userName:
            userObject = models.Users.objects.filter(userName=userName)
            if not userObject.exists():
                return JsonResponse({
                    "status": 404,
                    "message": "目标用户不存在"
                })
            userObject = userObject.first()

            mailList = models.Mails.objects.filter(receiver=userObject.userName)
            mailJsonList = []
            if not mailList.exists():
                return JsonResponse({
                    "status": 200,
                    "message": "成功",
                    "data": json.dumps(mailJsonList)
                })
            for mail in mailList:
                mailDict = {}
                mailDict["mailNo"] = mail.mailNo
                mailDict["sender"] = mail.sender
                mailDict["isRead"] = mail.isRead
                mailDict["subject"] = mail.subject
                mailJsonList.append(mailDict)

            return JsonResponse({
                "status": 200,
                "message": "成功",
                "data": json.dumps(mailJsonList)
            })
        else:
            return JsonResponse({
                "status": 404,
                "message": "表单未填写完整"
            })
    else:
        return JsonResponse({
            "status": 404,
            "message": "请求方式未注册"
        })


# Funtion: get mails have readed by id
# Return all attr
def GetReadMailsbyId(request):
    if request.method == "POST":
        mailNo = request.POST.get("mailNo", None)
        mailNo = int(mailNo)
        if mailNo:
            mailObject = models.Mails.objects.filter(mailNo=mailNo)
            if not mailObject.exists():
                return JsonResponse({
                    "status": 404,
                    "message": "目标邮件不存在"
                })
            mailObject = mailObject.first()

            return JsonResponse({
                "status": 200,
                "message": "成功",
                "data": model_to_dict(mailObject)
            })
        else:
            return JsonResponse({
                "status": 404,
                "message": "表单未填写完整"
            })
    else:
        return JsonResponse({
            "status": 404,
            "message": "请求方式未注册"
        })


# Function: get user static info
def GetStaticUsers(request):
    if request.method == "POST":
        nowDate = timezone.now().date()
        pastLimitDate = nowDate + relativedelta(days=-6)

        for i in range(7):
            userCountInfo = models.Users.objects\
                .filter(createDate=pastLimitDate)\
                .aggregate(userCount=Count("userNo"))

            mailObject = models.Mails.objects.filter(mailNo=mailNo)
            if not mailObject.exists():
                return JsonResponse({
                    "status": 404,
                    "message": "目标邮件不存在"
                })

            mailObject = mailObject.first()

        return JsonResponse({
            "status": 200,
            "message": "成功",
            "data": model_to_dict(mailObject)
        })
    else:
        return JsonResponse({
            "status": 404,
            "message": "请求方式未注册"
        })
    


# Function: get mail static info
def GetStaticMails(request):
    pass

# Class: user authority filter
# class UsersView(ListAPIView):
#     queryset = models.Users.objects.all()
#     serializer_class = customSerializers.UsersSerializer
#     filter_class = filters.UserAuthorityFilter
#     pagination_class = paginations.MyFormatResultsSetPagination


# Classes inherited from ModelViewSet which can generate RESTFUL URI
# @method_decorator(LoginAuthenticate, name='dispatch')
class UsersViewSet(viewsets.ModelViewSet):
    queryset = models.Users.objects.all().order_by('userNo')
    # 默认按userNo排序
    serializer_class = customSerializers.UsersSerializer
    pagination_class = paginations.MyFormatResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
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
