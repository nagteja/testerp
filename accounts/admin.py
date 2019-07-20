from django.contrib import admin

# Register your models here.

# Register your models here.
from accounts.models import Profile,Roles,Module,ModulePermission,FeaturesPermission,School,SchoolType

class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user','mobile','school']
	search_fields = ['user','mobile']

admin.site.register(Profile,ProfileAdmin)

class RolesAdmin(admin.ModelAdmin):
	list_display = ['school_id','roles','parent_territory','user_id']
	list_filter =  ['school_id','roles','parent_territory','user_id']
	search_fields =  ['school_id','roles','parent_territory','user_id']

admin.site.register(Roles,RolesAdmin)

class ModuleAdmin(admin.ModelAdmin):
	list_display = ['module','active','created_on']
	list_filter =  ['module','active','created_on']
	search_fields =  ['module','active','created_on']

admin.site.register(Module,ModuleAdmin)

class ModulePermissionAdmin(admin.ModelAdmin):
	list_display = ['school_id','roles','module','view','edit','create','delete','created_on','updated_at']
	list_filter =  ['school_id','roles','module','view','edit','create','delete','created_on']
	search_fields = ['school_id','roles','module','view','edit','create','delete','created_on']

admin.site.register(ModulePermission,ModulePermissionAdmin)


class FeaturesPermissionAdmin(admin.ModelAdmin):
	list_display = ['module','active','created_on']
	list_filter =  ['module','active','created_on']
	search_fields =  ['module','active','created_on']

admin.site.register(FeaturesPermission,FeaturesPermissionAdmin)

class SchoolAdmin(admin.ModelAdmin):
	list_display = ['school']
	list_filter =  ['school']
	search_fields =  ['school']

admin.site.register(School,SchoolAdmin)


class SchoolTypeAdmin(admin.ModelAdmin):
	list_display = ['name','created_on']
	list_filter =  ['name','created_on']
	search_fields =  ['name','created_on']

admin.site.register(SchoolType,SchoolTypeAdmin)