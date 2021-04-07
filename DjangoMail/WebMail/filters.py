import django_filters

from WebMail.models import CaseData, AccountInformation


# class CaseFilter(django_filters.rest_framework.FilterSet):
#     """
#     案例过滤器
#     """
#     userId = django_filters.NumberFilter(field_name='userId')

#     class Meta:
#         model = CaseData
#         fields = ['userId']


# class AccountInfoFilter(django_filters.rest_framework.FilterSet):
#     """
#     个人信息过滤器
#     """
#     authority = django_filters.CharFilter(field_name='authority')

#     class Meta:
#         model = AccountInformation
#         fields = ['authority']
