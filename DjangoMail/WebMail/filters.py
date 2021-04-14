import django_filters

from WebMail.models import Users, Mails


class UserAuthorityFilter(django_filters.rest_framework.FilterSet):
    authority = django_filters.NumberFilter(field_name="authorityValue", lookup_expr='lte')
    class Meta:
        model = Users  # 模型名
        fields = {
            'authorityValue':['gte','lte'],
        }
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
