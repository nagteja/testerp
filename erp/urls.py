from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from accounts import views 
from django.conf.urls.static import static
from django.conf import settings

app_name = 'erp'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='login'),
    #url(r'^login/$',auth_views.LoginView.as_view(template_name='login/login.html'), name="login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='login/logged_out.html'), name='logout'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(template_name= 'login/password_reset_form.html'), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name= 'login/password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name = 'login/password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(template_name='login/password_reset_complete.html'), name='password_reset_complete'),
    url(r'^accounts/',include('accounts.urls',namespace='accounts')),
    # url(r'^dynamicforms/',include('dynamicforms.urls',namespace='dynamicforms')),
    url(r'^dashboard/',include('dashboard.urls',namespace='dashboard')),
    url(r'^module/',include('module.urls',namespace='module')),
    url(r'^workflow/',include('workflow.urls',namespace='workflow')),
    url(r'^$', views.signUp, name='signup'),    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
