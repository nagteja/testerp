from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from module.models import DynamicForms
from accounts.models import Module,Profile
from tinymce.models import HTMLField
from accounts.models import User

class WorkFlow(models.Model):
	actions = models.CharField(_("Actions"),max_length=50,null=True)
	conditions = models.CharField(_("Conditions"),max_length=50,null=True)
	action_numb = models.IntegerField(null=True, blank=True)
	active = models.BooleanField(default=True)
	created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
	
	def __str__(self):
		return self.actions

class CreateRule(models.Model):
	module = models.CharField(max_length=50,blank=False)
	rule_name = models.CharField(_("Rule name"),max_length=50,blank=False)
	description = models.CharField(max_length=50,blank=False)
	dynamicforms = models.ForeignKey(DynamicForms,on_delete=models.CASCADE)
	created_on = models.DateTimeField(_("Created on"), auto_now_add=True)

	def __str__(self):
		return self.module

class WorkFlowCondition(models.Model):
	actions = models.CharField(_("Actions"),max_length=500,null=True)
	name = models.CharField(_("Dynamic form name"),max_length=200,null=True)
	action_numb = models.IntegerField(null=True, blank=True)
	active = models.IntegerField(null=True, blank=True)
	createrule = models.ForeignKey(CreateRule,on_delete=models.CASCADE)
	module = models.ForeignKey(Module,on_delete=models.CASCADE)
	created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
	revision = models.IntegerField(null=True, blank=True)
	
	def __str__(self):
		return self.actions

class WorkFlowWhen(models.Model):
	when = models.CharField(_("When"),max_length=50,null=True)
	description = models.CharField(_("description"),max_length=50,null=True)
	createrule = models.ForeignKey(CreateRule,on_delete=models.CASCADE)

	def __str__(self):
		return self.when

class WorkFlowLeads(models.Model):
	leads = models.CharField(_("Leads"),max_length=100,null=True)
	condition_arthimatic = models.CharField(_("Arthamatic operation"),max_length=50,null=True)
	condition = models.CharField(_("condition"),max_length=50,null=True)
	created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
	workflowwhen = models.ForeignKey(WorkFlowWhen,on_delete=models.CASCADE)

	def __str__(self):
		return self.condition_arthimatic

class DynamicFormOutput(models.Model):
	field_name  = models.CharField(max_length=500,null=True)
	field_value = models.CharField(max_length=500,null=True)
	condition_satisfies = models.IntegerField(default=0)
	dynamicforms = models.ForeignKey(DynamicForms,on_delete=models.CASCADE)

	def __str__(self):
		return self.field_name

class EmailTemplate(models.Model):
	template_name = models.CharField(max_length=120)
	subject = models.CharField(max_length=220)
	content =  models.TextField('Content')
	module_name = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True)
	school = models.ForeignKey(Profile, related_name='schoolname', on_delete=models.CASCADE)
	created_on = models.DateTimeField(default=datetime.now)
	modified_on = models.DateTimeField(default=datetime.now)

	def __str__(self):
		return self.template_name


class EmailNotification(models.Model):
	name = models.CharField(max_length=255, null=True, blank=True)
	email_recipients = models.EmailField(max_length=254,)
	additional_recipients = models.TextField(blank=True, null=True)
	email_template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE, null=True, blank=True)
	create_rule = models.ForeignKey(CreateRule,blank=True, null=True, on_delete=models.CASCADE, related_name='create_rule')
	send_as = models.EmailField(max_length=254,)
	created_on = models.DateTimeField(default=datetime.now)

	def __str__(self):
		return self.name

class EmailScheduleReport(models.Model):
	name = models.CharField(max_length=255, null=True, blank=True)
	create_rule = models.ForeignKey(CreateRule, on_delete=models.CASCADE, related_name='create_rule_schedule')
	email_template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE, null=True, blank=True)
	email_recipients = models.TextField(blank=True, null=True)
	# schedule_date = models.DateTimeField(default=datetime.now, null=True, blank=True)
	time_in_minute = models.IntegerField(default=0)
	time = models.IntegerField(default=0,null=True, blank=True)
	time_unit = models.CharField(max_length=255, null=True, blank=True)
	created_on = models.DateTimeField(default=datetime.now)

	def __str__(self):
		return self.name

class ScheduledEmailList(models.Model):
	module = models.ForeignKey(Module,on_delete=models.CASCADE)
	from_email = models.EmailField(max_length=200)
	to_email = models.EmailField(max_length=200)
	subject = models.CharField(max_length=200)
	content = HTMLField('Content')
	campaign_template = models.TextField(blank=True, null=True)
	created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.CASCADE)
	msg_id = models.CharField(max_length=255,null=True,blank=True)
	schedule_time = models.DateTimeField(default=datetime.now)
	status = models.CharField(max_length=200,null=True,blank=True)
	created_on = models.DateTimeField(default=datetime.now)

	def __str__(self):
		return self.from_email

