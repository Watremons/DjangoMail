from django.urls import path
from rest_framework.routers import DefaultRouter
from WebMail import views

router = DefaultRouter()

urlpatterns = [
    # # 渲染欢迎页，其后的页面跳转由前端负责
    # path('homepage/', views.HomePage, name="homepage"),
    # # 渲染模型介绍页，其后的页面跳转由前端负责
    # path('homepage/model/', views.ModelPage, name="model"),

    # # 身份验证请求
    # path('getIdentity/', views.GetIdentity, name="getIdentity"),

    # # 登录请求
    # path('signin/', views.Signin, name="signin"),

    # # 登出请求
    # path('logout/', views.Logout, name="logout"),

    # # 请求短信验证码
    # path('requestSmsCode/', views.RequestSmsCode, name="requestSmsCode"),

    # # 注册请求
    # path('signup/', views.Signup, name="signup"),

    # # 修改密码请求
    # path('changePwd/', views.ChangePwd, name="changePwd"),

    # # 忘记密码请求
    # path('forgetPwd/', views.ForgetPwd, name="forgetPwd"),

    # # 保存案例请求
    # path('saveCase/', views.SaveCase, name="saveCase"),

    # # 开始模拟请求
    # path('startSimulate/', views.StartSimulate, name="startSimulate"),

    # # 请求对应caseId的案例信息
    # path('getCaseInfo/', views.GetCaseInfos, name="getCaseInfo"),

    # # 用户管理数据请求
    # path('userManage/', views.GetUserInfos, name="userManage"),
    # path('generalUserManage/', views.GetGeneralUserInfos, name="generalUserManage"),
    # path('adminManage/', views.GetAdminInfos, name="adminManage"),

    # # 图表相关数据请求
    # path('topCity/', views.GetTopCityInfos, name="topCity"),
    # path('sexNum/', views.GetSexNum, name="sexNum"),
    # path('userCaseStat/', views.GetUserCaseStat, name="userCaseStat"),


    # 以下为对任意模型的增删改查列

    # 关于accountInfo的请求：
    # 无参数：get=list all,post=create new
    path('accountInfo/', views.AccountViewSet.as_view({'get': 'list', 'post': 'create'})),
    # 有参数：get=retrieve one,put=partial_update one,delete=delete one
    path('accountInfo/<int:pk>/', views.AccountViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'})),

    # 关于CaseData的请求
    # 无参数：get=list all,post=create new
    path('case/', views.CaseViewSet.as_view({'get': 'list', 'post': 'create'})),
    # 有参数：get=retrieve one,put=partial_update one,delete=delete one
    path('case/<int:pk>/', views.CaseViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'})),

    # 关于PersonalProfile的请求
    # 无参数：get=list all,post=create new
    path('profile/', views.PersonalProfileViewSet.as_view({'get': 'list', 'post': 'create'})),
    # 有参数：get=retrieve one,put=partial_update one,delete=delete one
    path('profile/<int:pk>/', views.PersonalProfileViewSet.as_view({'get': 'retrieve', 'put': 'partial_update', 'delete': 'destroy'})),
]
