# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from accounts.forms import SignUpForm
from django.core.exceptions import ValidationError
from accounts.models import Profile,Roles,Module,ModulePermission,FeaturesPermission,School,SchoolType
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from accounts.tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.files.storage import FileSystemStorage
import os.path

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                message = {'status': 200, 'message': "sucess", 'url':'accounts/dashboard/'} 
            else:
                message = {'status': 401, 'message': "Your account is not activated"} 
        else:
        	 message = {'status': 401, 'message': "Invalid login, please try again"} 
        return JsonResponse(message, safe=False)
    return render(request, 'login/login.html')

def loginSucess(request):
	return render(request, 'dashboard/index.html')

def signUp(request):
	if request.method == 'POST':
		user = User.objects.create(username=request.POST.get('email'),email=request.POST.get('email'),
			password=make_password(request.POST.get("password1")),first_name=request.POST.get('first_name'),last_name=request.POST.get('last_name'))
		user.refresh_from_db()  # load the profile instance created by the signal
		user.profile.mobile = request.POST.get('mobile')
		user.profile.school = request.POST.get('school')
		user.is_active = False
		user.save()
		raw_password = request.POST.get('password1')
		# user = authenticate(username=request.POST.get('email'), password=raw_password)
		# auth_login(request, user)
		# roles = Roles.objects.create(school_id=user.profile,roles='CEO',user_id=request.user)
		# roles.save() 
		current_site = get_current_site(request)
		mail_subject = 'Activate your Erp account.'
		message = render_to_string('login/account_activation_email.html', {
			'user': user,
			'domain': current_site.domain,
			'uid':urlsafe_base64_encode(force_bytes(user.pk)),
			'token':account_activation_token.make_token(user),
			})
		to_email = request.POST.get('email')
		email = EmailMessage(
		mail_subject, message, to=[to_email]
		)
		email.send()
		message = {'status': 200, 'message': "success"}
		return JsonResponse(message, safe=False)
	else:
		form = SignUpForm()
	return render(request, 'login/signup.html', {'form': form})

def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		auth_login(request, user)
		profile = Profile.objects.get(user=request.user)
		# Roles.objects.create(school_id=profile,roles='CEO',user_id=request.user) 
		rolesPost(request)
		return redirect('/accounts/school-profile')
	else:
		return HttpResponse('Activation link is invalid!')

def validateEmailUnique(value):
	exists = User.objects.filter(email=value)
	if exists:
		raise ValidationError("Email address %s already exists, must be unique" % value)

def mobileValidation(request):
	if request.method == 'POST':
		mobile = Profile.objects.filter(mobile=request.POST.get('mobile'))
	if mobile:
		for i in mobile:
			return HttpResponse('yes')   
	else:
		return HttpResponse('No')

def usernameValidation(request):
	if request.method == 'POST':
		username = User.objects.filter(username=request.POST.get('username'))
	if username:
		for i in username:
			return HttpResponse('yes')   
	else:
		return HttpResponse('No')

def emailValidation(request):
	if request.method == 'POST':
		email = User.objects.filter(email=request.POST.get('email'))
	if email:
		for i in email:
			return HttpResponse('yes')   
	else:
		return HttpResponse('No')


def schoolValidation(request):
	if request.method == 'POST':
		school = Profile.objects.filter(school=request.POST.get('school'))
	if school:
		for i in school:
			return HttpResponse('yes')   
	else:
		return HttpResponse('No')

def schoolDetails(request):
	school = Profile.objects.get(user_id = request.user)
	return school


def rolesPost(request):
	school = Profile.objects.get(user_id = request.user)
	role_creation = Roles.objects.create(school_id = school,roles='CEO',user_id=request.user)
	featurespermission = Module.objects.raw('SELECT `accounts_module`.`id`, `accounts_module`.`module`, `accounts_module`.`active`, `accounts_module`.`created_on` FROM `accounts_module` UNION SELECT `accounts_featurespermission`.`id`, `accounts_featurespermission`.`module`, `accounts_featurespermission`.`active`, `accounts_featurespermission`.`created_on` FROM `accounts_featurespermission`')
	for featurespermission in featurespermission:
		ModulePermission.objects.create(school_id =school,roles=role_creation,
				module=featurespermission.module,view='True',edit='True',create='True',delete='True')

@login_required
def roles(request):
	roles = Roles.objects.filter(user_id = request.user)
	school = Profile.objects.get(user_id = request.user)
	user_details = Profile.objects.select_related('user').filter(school=school.school)
	if request.method == 'POST':
		role = Roles.objects.filter(user_id = request.user).first()
		role_creation = Roles.objects.create(school_id = role.school_id,
			roles = request.POST.get('territoryname'),
			parent_territory = request.POST.get('parentterriority'),
			user_id = request.user)

		featurespermission = Module.objects.raw('SELECT `accounts_module`.`id`, `accounts_module`.`module`, `accounts_module`.`active`, `accounts_module`.`created_on` FROM `accounts_module` UNION SELECT `accounts_featurespermission`.`id`, `accounts_featurespermission`.`module`, `accounts_featurespermission`.`active`, `accounts_featurespermission`.`created_on` FROM `accounts_featurespermission`')
		for featurespermission in featurespermission:
			ModulePermission.objects.create(school_id =role.school_id,roles=role_creation,
					module=featurespermission.module,view='True' if(request.POST.get("view"))  else 'False',
					edit='True' if(request.POST.get("edit"))  else 'False',
					create='True' if(request.POST.get("create"))  else 'False',delete='True' if(request.POST.get("delete"))  else 'False')

	return render(request,'roles/user-permission.html',locals())


@login_required
def territory(request):
	roles = Roles.objects.filter(user_id=request.user)
	return JsonResponse(serializers.serialize('json', roles), safe=False)
	
@login_required
def createUser(request):
	school = Profile.objects.get(user_id = request.user)
	roles = Roles.objects.filter(user_id = request.user)
	user_details = Profile.objects.select_related('user').filter(school=school.school)
	if request.method == 'POST':
		user = User.objects.create(username=request.POST.get('email'),email=request.POST.get('email'),
			password=make_password(request.POST.get("password")),first_name=request.POST.get('first_name'),last_name=request.POST.get('last_name'))
		user.profile.mobile = request.POST.get("mobile")
		user.profile.user_role = request.POST.get("roles")
		user.profile.school = school.school
		user.profile.is_admin = 'True' if(request.POST.get("is_admin"))  else 'False'
		user.profile.gender = request.POST.get('gender')
		user.profile.dob = request.POST.get('date')
		user.profile.empid = request.POST.get('empid')
		user.profile.religion = request.POST.get('religion')
		user.profile.images = request.FILES.get('file')
		user.save()
	return render(request,'roles/user.html',locals())

@login_required
def selectRoles(request):
	roles = Roles.objects.filter(user_id = request.user).only('roles')
	return JsonResponse(serializers.serialize('json', roles), safe=False)

@login_required
def userPermission(request):
	sch_dl = schoolDetails(request)
	school = Profile.objects.filter(school=sch_dl.school).order_by('id')
	roles = Roles.objects.filter(school_id = school[0].id)
	module = Module.objects.raw('SELECT `accounts_module`.`id`, `accounts_module`.`module`, `accounts_module`.`active`, `accounts_module`.`created_on` FROM `accounts_module` UNION SELECT `accounts_featurespermission`.`id`, `accounts_featurespermission`.`module`, `accounts_featurespermission`.`active`, `accounts_featurespermission`.`created_on` FROM `accounts_featurespermission`')
	module_perm = ModulePermission.objects.filter(school_id =roles[0].school_id )
	if request.method == 'POST':
		roles_post = request.POST.get('roles')
	return render(request,'roles/user-permission.html',locals())


@login_required
def modulePermissions(request):
	roles = Roles.objects.filter(user_id = request.user,roles=request.POST.get("roles")).first()
	if request.method == 'POST' :
		permission = ModulePermission.objects.filter(school_id =roles.school_id,roles=roles.id,
			module=request.POST.get("module"))
		if not permission:
			ModulePermission.objects.create(school_id =roles.school_id,roles=roles,
				module=request.POST.get("module"),view='True' if(request.POST.get("view"))  else 'False',
				edit='True' if(request.POST.get("edit"))  else 'False',
				create='True' if(request.POST.get("create"))  else 'False',delete='True' if(request.POST.get("delete"))  else 'False')
		else :
			permission.update(
			view='True' if(request.POST.get("view"))  else 'False',
			edit='True' if(request.POST.get("edit"))  else 'False',
			create='True' if(request.POST.get("create"))  else 'False',delete='True' if(request.POST.get("delete"))  else 'False')
		# return redirect('accounts:user-permission')
		return userPermission(request)


def editUser(request,id):
	user = User.objects.select_related('profile').filter(id=id).first()
	return render(request,'roles/edit-roles.html',locals())



def schoolProfile(request):
	module_perm = permissionCheck(request,'School-Profile')
	# if module_perm.view == True :
	school_type = SchoolType.objects.all()
	sch_dl = schoolDetails(request)
	school = Profile.objects.filter(school=sch_dl.school).order_by('id')
	school_check = 	School.objects.filter(school=school[0].id)
	return render(request,'dashboard/school-profile.html',locals())
	# return HttpResponse("sorry babe dont have access")	

def schoolProfileEdit(request):
	school_type = SchoolType.objects.all()
	sch_dl = schoolDetails(request)
	school_check = 	School.objects.filter(school=sch_dl.id)
	if request.method == 'POST':
		if school_check:
			school_check.update(website=request.POST.get("website"),landline=request.POST.get("landline")
				,medium=request.POST.get("medium"),description=request.POST.get("description"),trust=request.POST.get("trust"),address=request.POST.get("address"),
				country=request.POST.get("country"),state=request.POST.get("state"),city=request.POST.get("city"),pin=request.POST.get("pin"),
				school_type=request.POST.get("school_type"),grade_from=request.POST.get("grade_from"),grade_to=request.POST.get("grade_to"),school_images=request.POST.get("school_images"))
		else :
			School.objects.create(school=sch_dl,website=request.POST.get("website"),landline=request.POST.get("landline")
				,medium=request.POST.get("medium"),description=request.POST.get("description"),trust=request.POST.get("trust"),address=request.POST.get("address"),
				country=request.POST.get("country"),state=request.POST.get("state"),city=request.POST.get("city"),pin=request.POST.get("pin"),
				school_type=request.POST.get("school_type"),grade_from=request.POST.get("grade_from"),grade_to=request.POST.get("grade_to"),school_images=request.POST.get("school_images"))
		return render(request,'dashboard/school-profile.html',locals())
	return render(request,'dashboard/school-profile-edit.html',locals())


def territoryValidation(request):
	if request.method == 'POST':
		schl = schoolDetails(request)
		territoryname = Roles.objects.filter(school_id=schl,roles=request.POST['territoryname'])
	if territoryname:
		for i in territoryname:
			return HttpResponse('yes')   
	else:
		return HttpResponse('No')

def permissionCheck(request,slug):
	sch_dl = Profile.objects.get(user_id = request.user)
	school = Profile.objects.filter(school=sch_dl.school).order_by('id')
	roles = Roles.objects.filter(user_id = sch_dl.user.id).first()
	module_perm = ModulePermission.objects.get(roles=roles,module=slug,school_id=school[0].id)
	return module_perm

def selectUser(request,id):
	sch_dl = schoolDetails(request)
	school = Profile.objects.filter(school=sch_dl.school).order_by('id')
	user_details = Profile.objects.select_related('user').filter(school=school[0].school)
	sel_user = User.objects.select_related('profile').get(id=id)
	return render(request,'roles/user.html',locals())

def selectUserUpdate(request,id):
	if request.method == "POST":
		user = User.objects.filter(id=id)
		user.update(first_name=request.POST.get('first_name_pro'),last_name=request.POST.get('last_name_pro'))
		if  request.POST.get('dob_pro'):
			date = request.POST.get('dob_pro')
		else :
			date = '0001-01-01'
		Profile.objects.filter(user=user[0].id).update(mobile=request.POST.get('mobile_pro'),user_role=request.POST.get('roles_pro'), 
			empid=request.POST.get('empid_pro'),gender=request.POST.get('gender_pro'),
			blood_group=request.POST.get('blood_group'),
			address=request.POST.get('address'),
			dob=date,country=request.POST.get('country_pro'),
			state=request.POST.get('state_pro'),city=request.POST.get('city_pro'))
	return selectUser(request,id)

@login_required
def myProfileView(request):
	myprofile = User.objects.filter(profile__user=request.user)
	if request.method == "POST":
		# myprofile.update(mobile=request.POST.get('mymobile'))
		Profile.objects.filter(user=request.user).update(mobile=request.POST.get('mymobile'),gender=request.POST.get('mygender'),
			blood_group=request.POST.get('mybloodgroup'),religion=request.POST.get('myreligion'),
			address=request.POST.get('myaddress'),
			dob=request.POST.get('mydob'),country=request.POST.get('mycountry'),
			state=request.POST.get('mystate'),city=request.POST.get('mycity'))
	return render(request, 'dashboard/my-profile.html',locals())