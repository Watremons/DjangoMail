# 引用Django库
from django.shortcuts import render
from django.http import JsonResponse
from django_redis import get_redis_connection
from django.utils import timezone
from django.core import paginator

# 引用DRF框架库
from rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets

# 引用项目文件
from WebMail import models
from WebMail import customSerializers
from WebMail import filters
from WebMail import paginations
# Create your views here.

# 设置日志文件的生成
logger = logging.getLogger("django")

# 登录验证函数，通过method_decorator作为装饰器装饰给各个视图
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


# 管理员验证函数，通过method_decorator作为装饰器装饰给各个视图
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


# 超级管理员验证函数，通过method_decorator作为装饰器装饰给各个视图
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


# 以下均为继承ModelViewSet类的视图集类，其中成员变量均为继承而来
# @method_decorator(LoginAuthenticate, name='dispatch')
class UsersViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = customSerializers.UsersSerializer


# @method_decorator(LoginAuthenticate, name='dispatch')
class MailsViewSet(viewsets.ModelViewSet):
    queryset = models.Mail.objects.all()
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
