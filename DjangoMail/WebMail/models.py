# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone


class Users(models.Model):
    userNo = models.AutoField(db_column='userNo', primary_key=True)
    userName = models.CharField(db_column='userName', max_length=50, blank=True)
    createDate = models.DateField(db_column='createDate', default=timezone.now)
    mailAddress = models.CharField(db_column='mailAddress', max_length=50, blank=True)
    authorityValue = models.IntegerField(db_column='authorityValue', default=0)  # 0:user 1:admin 2:superAdmin
    userState = models.BooleanField(db_column='userState', default=True)  # true:normal false:banned

    class Meta:
        db_table = 'Users'


class Mails(models.Model):
    mailNo = models.AutoField(db_column='mailNo', primary_key=True)
    receiver = models.CharField(db_column='receive', max_length=200, blank=True)
    sender = models.CharField(db_column='sender', max_length=200, blank=True)
    subject = models.CharField(db_column='subject', max_length=200, blank=True)
    copy = models.CharField(db_column='copy', max_length=200, blank=True)
    isRead = models.BooleanField(db_column='isRead', default=False)  # false:notRead true:haveRead
    isServed = models.IntegerField(db_column='authorityValue', default=0)  # 0:serving 1:haveServed 2:failToServe
    content = models.CharField(db_column='content', max_length=500, blank=True)
    rendOrReceiptDate = models.DateField(db_column='rendOrReceiptDate', default=timezone.now)
    userNo = models.ForeignKey(Users, models.CASCADE, db_column='userNo', default='1')

    class Meta:
        db_table = 'Mails'


class LoginData(models.Model):
    userId = models.OneToOneField(Users, models.CASCADE, db_column='userId', primary_key=True)
    userPassword = models.CharField(db_column='userPassword', max_length=32)
    salt = models.CharField(max_length=20)

    class Meta:
        db_table = 'LoginData'


class Contacts(models.Model):
    contactNo = models.AutoField(db_column='contactNo', primary_key=True)
    contactName = models.CharField(db_column='userName', max_length=50)
    tel = models.CharField(db_column='tel', max_length=50, blank=True)
    mailAddress = models.CharField(db_column='mailAddress', max_length=50, blank=True)
    userNo = models.ForeignKey(Users, models.CASCADE, db_column='userNo', default='1')

    class Meta:
        db_table = 'Contacts'


class Attachments(models.Model):
    attachmentNo = models.AutoField(db_column='attachmentNo', primary_key=True)
    attachmentName = models.CharField(db_column='attachmentName', max_length=100)
    savedAddress = models.CharField(db_column='savedAddress', max_length=200)
    attachmentSize = models.FloatField(db_column='attachmentSize')
    mailNo = models.ForeignKey(Mails, models.CASCADE, db_column='mailNo', default='1')

    class Meta:
        db_table = 'Attachments'
