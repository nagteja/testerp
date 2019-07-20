from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from accounts import views 

app_name = 'accounts'

urlpatterns = [
    url(r'^signup/$', views.signUp, name='signup'),
    url(r'^dashboard/$', views.loginSucess, name='dashboard'),
    url(r'^mobilevalidation/$',views.mobileValidation,name = 'mobilevalidation'),
    url(r'^usernamevalidation/$',views.usernameValidation,name = 'usernamevalidation'),
    url(r'^emailvalidation/$',views.emailValidation,name = 'emailvalidation'),
    url(r'^schoolvalidation/$',views.schoolValidation,name = 'schoolvalidation'),
    url(r'^roles/$',views.roles,name = 'roles'),
    url(r'^territory/$',views.territory,name = 'territory'),
    url(r'^create-user/$',views.createUser,name = 'create-user'),
    url(r'^select-roles/$',views.selectRoles,name = 'select-roles'),
    url(r'^user-permission/$',views.userPermission,name = 'user-permission'),
    url(r'^module-permissions/$',views.modulePermissions,name = 'module-permissions'),
    url(r'^edit-user/(?P<id>[0-9]+)/$',views.editUser,name = 'edit-user'),
    url(r'^school-profile/$', views.schoolProfile, name='school-profile'),
    url(r'^school-profile-edit/$', views.schoolProfileEdit, name='school-profile-edit'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^territoryvalidation/$',views.territoryValidation,name = 'territoryvalidation'),
    url(r'^select-user/(?P<id>[0-9]+)/$',views.selectUser,name = 'edit-user'),
    url(r'^select-user-update/(?P<id>[0-9]+)/$',views.selectUserUpdate,name = 'edit-user-update'),
    # url(r'^permissioncheck/$',views.permissionCheck,name = 'permissioncheck'),
    url(r'^myprofile/$', views.myProfileView, name='myprofile'),
]


