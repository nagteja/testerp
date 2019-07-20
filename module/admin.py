from django.contrib import admin

# Register your models here.
from module.models import DynamicForms,SavedForms,SampleForms

class DynamicFormsAdmin(admin.ModelAdmin):
	list_display = ['school_id','module','form_name','revision']
	list_filter =  ['school_id','module','form_name','revision']
	search_fields =  ['school_id','module','form_name','revision']

admin.site.register(DynamicForms,DynamicFormsAdmin)

class SavedFormsAdmin(admin.ModelAdmin):
	list_display = ['school_id','dynamic_forms','user_id','revision','created_on']
	list_filter =  ['school_id','dynamic_forms','user_id','revision','created_on']
	search_fields =  ['school_id','dynamic_forms','user_id','revision','created_on']

admin.site.register(SavedForms,SavedFormsAdmin)

admin.site.register(SampleForms)