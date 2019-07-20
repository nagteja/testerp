from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView
from module import views 

app_name = 'module'

urlpatterns = [
    url(r'^dynamicforms/(?P<slug>.*)/$', views.dynamicForms, name='dynamicforms'),
    url(r'^create/(?P<slug>.*)/$',views.createForms,name = 'createforms'),
    url(r'^list/(?P<slug>.*)/$',views.listForms,name = 'list'),
    url(r'^listformview/(?P<id>[0-9]+)/$',views.listFormView,name = 'listformview'),
    url(r'^uploadforms/$',views.fileUpload,name = 'uploadforms'),
    url(r'^form-view/(?P<slug>.*)/$',views.formView,name = 'form-view'),
    url(r'^form-individual/(?P<id>[0-9]+)/$',views.formIndividualView,name = 'form-individual'),
    url(r'^form-individual-profile/(?P<id>[0-9]+)/$',views.formIndividualProfile,name = 'form-individual-profile'),
    url(r'^saved-forms/$',views.savedFormsview,name = 'saved-forms'),
]

