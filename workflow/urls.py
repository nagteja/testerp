from django.conf.urls import url, include
from workflow import views

app_name = 'workflow'

urlpatterns = [
    url(r'^$', views.workFlow, name='workflow'),
    url(r'^workflowsave/(?P<id>[0-9]+)/$',views.workFlowSave,name = 'workflowsave'),
    url(r'^email-notification/(?P<id>[0-9]+)/$',views.emailNotification,name = 'email-notification'),
    url(r'^email-schedule/(?P<id>[0-9]+)/$',views.emailSchedule,name = 'email-schedule'),
    url(r'^create-template/$',views.createTemplate,name = 'create-template'),
    url(r'^when-update/(?P<id>[0-9]+)/$',views.whenUpdate,name = 'when-update'),
    url(r'^condition-edit/(?P<id>[0-9]+)/(?P<rule_id>[0-9]+)/$',views.conditionEdit,name = 'condition-edit'),
    url(r'^condition-update/(?P<id>[0-9]+)/(?P<rule_id>[0-9]+)/$',views.conditionUpdate,name = 'condition-update'),
    url(r'^new-workflow-condition/(?P<id>[0-9]+)/$',views.newWorkflowConditoin,name = 'new-workflow-condition'),
    url(r'^condition-delete/(?P<id>[0-9]+)/(?P<rule_id>[0-9]+)/$',views.conditionDelete,name = 'condition-delete'),

    # url(r'^workFlowSave/(?P<id>[0-9]+)/$', views.workFlowSave, name='workFlowSave'),
    # url(r'^test/$', views.test, name='test'),

]