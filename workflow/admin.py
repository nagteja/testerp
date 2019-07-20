from django.contrib import admin
from workflow.models import WorkFlow,WorkFlowWhen,WorkFlowLeads,CreateRule,WorkFlowCondition,DynamicFormOutput,EmailNotification,EmailScheduleReport,ScheduledEmailList,EmailTemplate

class WorkFlowAdmin(admin.ModelAdmin):
	list_display = ['actions','conditions','active','action_numb']
	list_filter = ['actions','conditions','active']
	search_fields = ['actions','conditions','active']

admin.site.register(WorkFlow,WorkFlowAdmin)

class WorkFlowWhenAdmin(admin.ModelAdmin):
	list_display = ['when','description']
	list_filter = ['when','description']
	search_fields = ['when','description']

admin.site.register(WorkFlowWhen,WorkFlowWhenAdmin)

class WorkFlowLeadsAdmin(admin.ModelAdmin):
	list_display = ['leads','condition_arthimatic','workflowwhen']
	list_filter = ['leads','condition_arthimatic']
	search_fields = ['leads','condition_arthimatic']

admin.site.register(WorkFlowLeads,WorkFlowLeadsAdmin)

class DynamicFormOutputAdmin(admin.ModelAdmin):
	list_display = ['field_name','field_value','condition_satisfies']
	list_filter = ['field_name','field_value','condition_satisfies']
	search_fields = ['field_name','field_value','condition_satisfies']

admin.site.register(DynamicFormOutput,DynamicFormOutputAdmin)

class CreateRuleAdmin(admin.ModelAdmin):
    list_display = ['module','rule_name','description']
    list_filter = ['module','rule_name','description']
    search_fields = ['module','rule_name','description']

admin.site.register(CreateRule,CreateRuleAdmin)

class WorkFlowConditionAdmin(admin.ModelAdmin):
    list_display = ['actions','name','active','action_numb']
    list_filter = ['actions','name','active','action_numb']
    search_fields = ['actions','name','active','action_numb']

admin.site.register(WorkFlowCondition,WorkFlowConditionAdmin)

class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ['email_recipients','name','send_as','create_rule']
    list_filter = ['email_recipients','name','send_as','create_rule']
    search_fields = ['email_recipients','name','send_as','create_rule']

admin.site.register(EmailNotification,EmailNotificationAdmin)

class EmailScheduleReportAdmin(admin.ModelAdmin):
	list_display = ['create_rule','name','email_recipients']
	list_filter = ['create_rule','name','email_recipients']
	search_fields = ['create_rule','name','email_recipients']

admin.site.register(EmailScheduleReport,EmailScheduleReportAdmin)

class ScheduledEmailListAdmin(admin.ModelAdmin):
	list_display = ['module','from_email','to_email','msg_id','schedule_time','status']
	list_filter = ['module','from_email','to_email','msg_id','schedule_time','status']
	search_fields = ['module','from_email','to_email','msg_id','schedule_time','status']

admin.site.register(ScheduledEmailList,ScheduledEmailListAdmin)

class EmailTemplateAdmin(admin.ModelAdmin):
	list_display = ('template_name', 'subject', 'module_name', 'created_on')
	list_filter = ['created_on']
	search_fields = ['template_name']

admin.site.register(EmailTemplate, EmailTemplateAdmin)