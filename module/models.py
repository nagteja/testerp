from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from accounts.models import Module,Profile


class DynamicForms(models.Model):
	module = models.ForeignKey(Module, blank=True, null=True, on_delete=models.CASCADE)
	school_id = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE)
	user_id =  models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
	form_name = models.CharField(_('form name'),max_length=100,blank=True)
	form_field = models.TextField(_('Template details for the form'), blank=True)
	revision = models.IntegerField(_('revision id'),blank=True)

	class Meta:
		ordering = ['revision']

	def __unicode__(self):
		return self.form_name

class SavedForms(models.Model):
	dynamic_forms = models.ForeignKey(DynamicForms, blank=True, null=True, related_name="dynamic_forms", on_delete=models.CASCADE)
	school_id = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE)
	user_id =  models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
	saved_form_details = models.TextField(_('Form data'), blank=True, null=True)
	revision = models.IntegerField(_('revision id'),blank=True)
	status_wrkflw = models.BooleanField(default=False) 
	created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
	
	def __unicode__(self):
		return self.dynamic_forms
	

class SampleForms(models.Model):
	form_name = models.CharField(_('form name'),max_length=100)
	form_field = models.TextField(_('form_field'), blank=True, null=True)
	revision = models.IntegerField(_('revision id'),blank=True)
	
	def __unicode__(self):
		return self.form_name