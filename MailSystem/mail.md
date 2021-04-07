<!--
 * @Author: One_Random
 * @Date: 2020-04-18 12:14:35
 * @LastEditors: One_Random
 * @LastEditTime: 2020-05-24 19:57:21
 * @FilePath: /mail/mail.md
 * @Description: Copyright © 2020 One_Random. All rights reserved.
--> 
# 简易模拟邮箱
## 0.环境
### &emsp;a.服务器
&emsp;&emsp;&emsp;阿里云服务器 Linux x86_64 Ubuntu 16.04
### &emsp;b.开发语言
&emsp;&emsp;&emsp;服务端：python
&emsp;&emsp;&emsp;客户端：java-android
### &emsp;c.数据库
&emsp;&emsp;&emsp;mysql数据库

## 1.数据库
### &emsp;a.设计
&emsp;&emsp;&emsp;user(<u>userID</u>, username, password, type, usable);

&emsp;&emsp;&emsp;sendmail(<u>mailID</u>, userID, heloFrom, ip, mailFrom, rcptTo, content, time);

&emsp;&emsp;&emsp;recvmail(<u>mailID</u>, userID, heloFrom, ip, mailFrom, rcptTo, content, time);

## 2.服务端
### &emsp;a.smtp服务器
&emsp;&emsp;&emsp;1)状态图

![状态图](http://101.132.145.207:8080/upload/One_Random/smtp.png)

graph TB
 WAITING --> |'helo ...'| AUTH_AFTER 
 WAITING --> |'ehlo ...'| AUTH_BEFORE
 AUTH_BEFORE --> |'helo ...'| AUTH_AFTER
 AUTH_BEFORE --> |'ehlo ...'| AUTH_BEFORE
 AUTH_BEFORE --> |'auth login'| AUTH_LOGIN
 AUTH_LOGIN --> |any input| AUTH_USER
 AUTH_USER --> |any input & auth ok| AUTH_AFTER
 AUTH_USER --> |any input & auth fail| AUTH_BEFORE
 AUTH_AFTER --> |"'ehlo ... ' | 'helo ...'"| AUTH_AFTER
 AUTH_AFTER --> |'auth login'| AUTH_LOGIN
 AUTH_AFTER --> |'mail from:<...>'| MAILFROM
 MAILFROM --> |"'ehlo ...'| 'helo ...'"| MAILFROM
 MAILFROM --> |'mail from:<...>'| MAILFROM
 MAILFROM --> |'rcpt to:<...>'| RCPTTO --> |'data'| DATA
 RCPTTO --> |"'ehlo ...'| 'helo ...'"| RCPTTO
 RCPTTO --> |'rcpt to:<...>'| RCPTTO
 DATA --> |'<CR><LF>.<CR><LF>' & send mail| AUTH_AFTER
 DATA --> |other input| DATA

 WAITING --> |'quit'| QUIT
 AUTH_BEFORE --> |'quit'| QUIT
 AUTH_AFTER --> |'quit'| QUIT
 MAILFROM --> |'quit'| QUIT
 RCPTTO --> |'quit'| QUIT


# b25lX3JhbmRvbUAxNjMuY29t
# Q05UTVVKWkVWTk9KWUZXQw==

# T25lX1JhbmRvbQ==
# YWRtaW4=

# T25lX1JhbmRvbUB0ZXN0LmNvbQ==

# dGVzdEB0ZXN0LmNvbQ==

#One_Random@163.com
#CNTMUJZEVNOJYFWC