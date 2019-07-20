from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from accounts.models import Profile,Roles,Module,ModulePermission
from django.contrib.auth.models import User
from module.models import DynamicForms,SavedForms,SampleForms
from workflow.models import DynamicFormOutput,CreateRule,WorkFlowWhen,WorkFlowLeads,EmailNotification,ScheduledEmailList,EmailScheduleReport,EmailTemplate
from django.core.files.storage import FileSystemStorage
from module.mailin import Mailin 
from django.utils import timezone
from datetime import timedelta
import json
from django.contrib.auth.decorators import login_required

# Create your views here.

def schoolDetails(request):
	sch_dl = Profile.objects.get(user_id = request.user)
	school = Profile.objects.filter(school=sch_dl.school).order_by('id')
	roles = Roles.objects.filter(user_id = school[0].user.id).first()
	return roles

@login_required
def dynamicForms(request,slug):
	roles = schoolDetails(request)
	module_perm = ModulePermission.objects.get(roles=roles,module=slug,school_id=roles.school_id)
	if module_perm.view == True :
		module = Module.objects.get(module=slug)
		try :
			questions = DynamicForms.objects.get(form_name=slug,school_id=roles.school_id)
		except DynamicForms.DoesNotExist:
			questions = None
		if not questions:
			questions = SampleForms.objects.get(form_name=slug)
		return render(request,'module/index.html',locals())
	return HttpResponse('sorry contact admin')

@login_required
def createForms(request,slug):
	roles = schoolDetails(request)
	module = Module.objects.get(module=slug)
	if request.method == 'POST':
		display_form = DynamicForms.objects.filter(form_name=request.POST.get('formname'),school_id=roles.school_id)
		if not display_form:
			dynamicforms = DynamicForms.objects.create(
				module_id = module.id,
				school_id = roles.school_id,
				user_id = request.user,
				form_name = request.POST.get('formname'),
				revision = '1',
				form_field = request.POST.get('form_details')
				)
		else :
			if display_form[0].form_field != request.POST.get('form_details'):
				dynamicforms = display_form.update(form_field = request.POST.get('form_details'),revision = display_form[0].revision +1)
		return render(request,'module/previewtemplate.html',locals())
	return render(request,'module/index.html',locals())

@login_required
def listForms(request,slug):
	sch_dl = Profile.objects.get(user_id = request.user)
	school = Profile.objects.filter(school=sch_dl.school).order_by('id')
	listform = DynamicForms.objects.filter(school_id=school[0].id,form_name=slug).order_by('-revision')
	return listFormView(request,listform[0].id)

@login_required
def listFormView(request,id):
	display_form = DynamicForms.objects.get(id=id)
	if request.method == 'POST':
		savedforms = SavedForms.objects.create(
				dynamic_forms = display_form,
				school_id = display_form.school_id,
				user_id = request.user,
				saved_form_details = request.POST.get('saved_form_details'),
				revision = display_form.revision,
			)
		savedforms.save()
		createrule = CreateRule.objects.filter(dynamicforms=display_form)
		for createrule in createrule:
			if createrule:
				workflowwhen = WorkFlowWhen.objects.get(createrule=createrule)
				if workflowwhen.when == 'Create':
					sf_to_wf = SavedForms.objects.filter(id=savedforms.id)
					for i in sf_to_wf:
						json_data = json.loads(i.saved_form_details)
						for j in range(len(json_data)):
							workflowleads = WorkFlowLeads.objects.filter(workflowwhen=workflowwhen)
							for workflowleads in workflowleads:
								a = "is"
								b = "isn't"
								c = "contains"
								d = "doesn't contain"
								e = "start with"
								f = "ends with"
								g = "is empty"
								h = "is not empty"
								if(a == workflowleads.condition_arthimatic):
									if(json_data[j]['name'] == workflowleads.leads):
										if(json_data[j]['value'] == workflowleads.condition):
											DynamicFormOutput.objects.create(field_name  = json_data[j]['name'],field_value = json_data[j]['value'],dynamicforms =  display_form,condition_satisfies=1)
										else:
											DynamicFormOutput.objects.create(field_name  = json_data[j]['name'],field_value = json_data[j]['value'],dynamicforms =  display_form,condition_satisfies=0)
								elif(b == workflowleads.condition_arthimatic):
									if(json_data[j]['name'] == workflowleads.leads):
										if(json_data[j]['value'] != workflowleads.condition):
											DynamicFormOutput.objects.create(field_name  = json_data[j]['name'],field_value = json_data[j]['value'],dynamicforms =  display_form,condition_satisfies=1)
										else:
											DynamicFormOutput.objects.create(field_name  = json_data[j]['name'],field_value = json_data[j]['value'],dynamicforms =  display_form,condition_satisfies=0)
								elif(c == workflowleads.condition_arthimatic):	
									if(json_data[j]['name'] == workflowleads.leads):
										if json_data[j]['value'] in workflowleads.condition:
											DynamicFormOutput.objects.create(field_name  = json_data[j]['name'],field_value = json_data[j]['value'],dynamicforms =  display_form,condition_satisfies=1)
										else:
											DynamicFormOutput.objects.create(field_name  = json_data[j]['name'],field_value = json_data[j]['value'],dynamicforms =  display_form,condition_satisfies=0)
								elif(d == workflowleads.condition_arthimatic):	
									if(json_data[j]['name'] == workflowleads.leads):
										if json_data[j]['value'] not in workflowleads.condition:
											DynamicFormOutput.objects.create(field_name  = json_data[j]['name'],field_value = json_data[j]['value'],dynamicforms =  display_form,condition_satisfies=1)
										else:
											DynamicFormOutput.objects.create(field_name  = json_data[j]['name'],field_value = json_data[j]['value'],dynamicforms =  display_form,condition_satisfies=0)
								elif(e == workflowleads.condition_arthimatic):	
									if(json_data[j]['name'] == workflowleads.leads):
										if json_data[j]['value'].startswith(workflowleads.leads):
											DynamicFormOutput.objects.create(field_name  = json_data[j]['name'],field_value = json_data[j]['value'],dynamicforms =  display_form,condition_satisfies=1)
										else:
											DynamicFormOutput.objects.create(field_name  = json_data[j]['name'],field_value = json_data[j]['value'],dynamicforms =  display_form,condition_satisfies=0)
								elif(f == workflowleads.condition_arthimatic):	
									if(json_data[j]['name'] == workflowleads.leads):
										if json_data[j]['value'].endswith(workflowleads.leads):
											DynamicFormOutput.objects.create(field_name  = json_data[j]['name'],field_value = json_data[j]['value'],dynamicforms =  display_form,condition_satisfies=1)
										else:
											DynamicFormOutput.objects.create(field_name  = json_data[j]['name'],field_value = json_data[j]['value'],dynamicforms =  display_form,condition_satisfies=0)
								elif(g == workflowleads.condition_arthimatic):	
									if(json_data[j]['name'] == workflowleads.leads):
										if not workflowleads.leads:
											DynamicFormOutput.objects.create(field_name  = json_data[j]['name'],field_value = json_data[j]['value'],dynamicforms =  display_form,condition_satisfies=1)
										else:
											DynamicFormOutput.objects.create(field_name  = json_data[j]['name'],field_value = json_data[j]['value'],dynamicforms =  display_form,condition_satisfies=0)
								elif(h == workflowleads.condition_arthimatic):	
									if(json_data[j]['name'] == workflowleads.leads):
										if  workflowleads.leads:
											DynamicFormOutput.objects.create(field_name  = json_data[j]['name'],field_value = json_data[j]['value'],dynamicforms =  display_form,condition_satisfies=1)
										else:
											DynamicFormOutput.objects.create(field_name  = json_data[j]['name'],field_value = json_data[j]['value'],dynamicforms =  display_form,condition_satisfies=0)
						check_value = []
						dynamic_output = DynamicFormOutput.objects.filter(dynamicforms = display_form)
						for dynamic_output in dynamic_output:
							check_value.append(dynamic_output.condition_satisfies)
						if check_value.count(check_value[0]) == len(check_value):
							sf_to_wf.update(status_wrkflw='True')
							emailnotifi = EmailNotification.objects.get(create_rule=createrule)
							template = EmailTemplate.objects.get(id=emailnotifi.email_template.id)
							mail = Mailin("https://api.sendinblue.com/v2.0","MPSyR0F65Acj8fnQ")
							data = { "to" : {emailnotifi.email_recipients:emailnotifi.name},
							"from" : [emailnotifi.send_as,'School Serv Admission'],
							"subject" : template.subject,
							"html" : template.content,
							}
							result = mail.send_email(data)
							ScheduledEmailList.objects.create(
											module = display_form.module,
											from_email = emailnotifi.send_as,
											to_email = emailnotifi.email_recipients,
											subject = 'temp.subject',
											campaign_template = 'email_note.email_template',
											created_by = request.user,
											msg_id = result['data']['message-id'],
											status = result['code'],
										)
							email_schedule = EmailScheduleReport.objects.filter(create_rule=createrule)
							if email_schedule:
								for email_schedule in email_schedule:
									schedule_value = timezone.localtime(sf_to_wf[0].created_on) + timedelta(minutes=email_schedule.time_in_minute)
									ScheduledEmailList.objects.create(
												module = display_form.module,
												from_email = emailnotifi.send_as,
												to_email = email_schedule.email_recipients,
												subject = 'temp.subject',
												campaign_template = 'email_note.email_template',
												created_by = request.user,
												schedule_time = schedule_value,
												status = 'Scheduled',
											)
								return HttpResponse('Data Saved')
						else:
							sf_to_wf.update(status_wrkflw='False')
		return HttpResponseRedirect('/module/form-view/%s/' % display_form.module.module)				
	return render(request,'module/displaytemplate.html',locals())

@login_required
def fileUpload(request):	
	if request.method == 'POST' and request.FILES['image']:
		myfile = request.FILES['image']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		return HttpResponse(uploaded_file_url)

@login_required
def formView(request,slug):
	sch_dl = Profile.objects.get(user_id = request.user)
	school = Profile.objects.filter(school=sch_dl.school).order_by('id')
	module = Module.objects.get(module=slug)
	dynamic_forms = DynamicForms.objects.get(form_name=slug,school_id=school[0].id)
	form_view = SavedForms.objects.raw("SELECT * FROM `module_savedforms`  LEFT OUTER JOIN `module_dynamicforms`ON (`module_savedforms`.`dynamic_forms_id` = `module_dynamicforms`.`id`)  INNER JOIN  `accounts_module` ON (`module_dynamicforms`.`module_id` = `accounts_module`.`id`) WHERE `module_dynamicforms`.`module_id`= %s and `module_savedforms`.`school_id_id`= %s" %(module.id,school[0].id))
	# final_view = []
	# for i in range(len(form_view)):
	# 	final_dictionary = eval(form_view[i].saved_form_details) 
	# 	final_view.append(final_dictionary)
	# len_final = len(final_view)
	return render(request,'module/form-view.html',locals())

@login_required
def formIndividualView(request,id):
	answers = SavedForms.objects.raw("SELECT * FROM `module_savedforms`  LEFT OUTER JOIN `module_dynamicforms`ON (`module_savedforms`.`dynamic_forms_id` = `module_dynamicforms`.`id`)  WHERE `module_savedforms`.`id`= %s" %id)
	if request.method == 'POST':
		answer = SavedForms.objects.filter(id=id).update(saved_form_details=request.POST.get('saved_form_details'))
	return render(request,'module/form-inividual-view.html',locals())

def savedFormsview(request):
	all_forms = SampleForms.objects.all()
	return render(request,'module/all-forms.html',locals())

@login_required
def formIndividualProfile(request,id):
	answers = SavedForms.objects.raw("SELECT * FROM `module_savedforms`  LEFT OUTER JOIN `module_dynamicforms`ON (`module_savedforms`.`dynamic_forms_id` = `module_dynamicforms`.`id`)  WHERE `module_savedforms`.`id`= %s" %id)
	if request.method == 'POST':
		answer = SavedForms.objects.filter(id=id).update(saved_form_details=request.POST.get('saved_form_details'))
	return render(request,'module/form-inividual-profile.html',locals())
