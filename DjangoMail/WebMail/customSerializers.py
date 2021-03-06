from rest_framework import serializers
from WebMail.models import Users, Contacts
from WebMail.models import Mails, Attachments


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class MailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mails
        fields = '__all__'


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = '__all__'


class AttachmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachments
        fields = '__all__'


# 如何添加只读字段
# class PersonalProfileSerializer(serializers.ModelSerializer):
#     # 为头像URL生成一个只读字段，返回给前端
#     avatarUrl = serializers.SerializerMethodField("GetAvatarUrl")

#     # DRF对于只读字段SerializerMethodField的生成函数
#     def GetAvatarUrl(self, obj):
#         return "http://47.112.227.85" + obj.avatar.url

#     class Meta:
#         model = PersonalProfile
#         fields = '__all__'
