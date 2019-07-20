# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

User._meta.get_field('email')._unique = True

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	mobile = models.CharField(max_length=14,null=True, blank=True, unique=True)
	school = models.CharField(max_length=255,null=True, blank=True)
	user_role = models.CharField(_('User Roles'),max_length=100, default='CEO')
	is_admin =  models.BooleanField(default=False)
	gender = models.CharField(max_length=50,null=True, blank=True)
	dob = models.DateField(_("Date"),null=True,blank=True)
	empid = models.CharField(max_length=255,null=True, blank=True)
	religion = models.CharField(max_length=255,null=True, blank=True)
	active = models.BooleanField(default=True)
	images = models.ImageField(upload_to='accounts', null=True, blank=True)
	blood_group = models.CharField(max_length=20,null=True, blank=True)
	address = models.TextField(null=True,blank=True)
	country = models.CharField(max_length=40, default='India')
	state = models.CharField(max_length=30, null=True, blank=True)
	city = models.CharField(max_length=30, null=True, blank=True)


def __unicode__(self):
	return self.user

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class School(models.Model):
	school = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE,related_name="schoolid")
	website = models.URLField(null=True,blank=True)
	landline = models.CharField(max_length=30,null=True,blank=True)
	medium = models.CharField(max_length=30, null=True, blank=True)
	description = models.TextField(null=True,blank=True)
	trust = models.CharField(max_length=40, null=True, blank=True)
	address = models.TextField(null=True,blank=True)
	country = models.CharField(max_length=40, default='India')
	state = models.CharField(max_length=30, null=True, blank=True)
	city = models.CharField(max_length=30, null=True, blank=True)
	pin = models.CharField(max_length=10,null=True,blank=True)
	school_type = models.CharField(max_length=50,null=True,blank=True)
	grade_from = models.CharField(max_length=10,null=True,blank=True)
	grade_to = models.CharField(max_length=10,null=True,blank=True)
	school_images = models.CharField(max_length=100,null=True,blank=True)

	def __unicode__(self):
		return self.school

class Roles(models.Model):
	school_id = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE)
	roles = models.CharField(_('Roles'),max_length=100, default='CEO')
	parent_territory =  models.CharField(_('Parent Territory'),max_length=100)
	user_id =  models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
	created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
	
def __unicode__(self):
	return self.roles

class Module(models.Model):
	module = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	active = models.BooleanField(default=True)
	created_on = models.DateTimeField(_("Created on"), auto_now_add=True)

	def __unicode__(self):
		return self.module

class ModulePermission(models.Model):
	school_id = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE)
	module = models.CharField(max_length=100)
	roles = models.ForeignKey(Roles, blank=True, null=True, on_delete=models.CASCADE)
	view = models.BooleanField(default=False)
	create = models.BooleanField(default=False)
	edit = models.BooleanField(default=False)
	delete = models.BooleanField(default=False)
	created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.module

class FeaturesPermission(models.Model):
	module = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	active = models.BooleanField(default=True)
	created_on = models.DateTimeField(_("Created on"), auto_now_add=True)

	def __unicode__(self):
		return self.permission


class SchoolType(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)

    def __unicode__(self):
        return self.name
