from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from workflow.models import WorkFlow,WorkFlowWhen,WorkFlowLeads,CreateRule,WorkFlowCondition,DynamicFormOutput,EmailNotification,EmailScheduleReport,EmailTemplate
from module.models import DynamicForms
from django.urls import reverse
from accounts.models import Module,Profile
import json

def workFlow(request):
	school = Profile.objects.get(user_id = request.user)
	module = DynamicForms.objects.filter(school_id = school)
	createrule = CreateRule.objects.raw('SELECT * FROM `workflow_createrule` LEFT OUTER JOIN `module_dynamicforms`ON (`module_dynamicforms`.`id` = `workflow_createrule`.`dynamicforms_id`)INNER JOIN `accounts_profile` ON (`module_dynamicforms`.`school_id_id` = `accounts_profile`.`id`) WHERE `accounts_profile`.`id` = %s' %school.id)
	if request.method == 'POST':
		module_id = Module.objects.get(module = request.POST['module'])
		dynamicforms = DynamicForms.objects.get(module = module_id,school_id = school)
		createrule = CreateRule.objects.create(module = request.POST['module'],
			rule_name = request.POST['rule_name'],
			description = request.POST['description'],
			dynamicforms = dynamicforms)
		createrule.save()
		rule = CreateRule.objects.get(id = createrule.id)
		workflocondition = WorkFlowCondition.objects.filter(module = module_id,revision=rule.dynamicforms.revision)
		if  not workflocondition:
			dynamicforms = DynamicForms.objects.filter(module = module_id,revision = rule.dynamicforms.revision)
			for i in dynamicforms:
				json_data = json.loads(i.form_field)
				for j in range(len(json_data)):
					if 'name'  in json_data[j]:
						workflowcondition = WorkFlowCondition.objects.create(
							actions = json_data[j]['label'],
							name = json_data[j]['name'],
							action_numb = 1,
							active = 1,
							module = module_id,
							createrule_id = createrule.id,
							revision = rule.dynamicforms.revision )
		
		recordaction = WorkFlow.objects.filter(action_numb=1)
		score = WorkFlow.objects.filter(action_numb=2)
		leads = WorkFlowCondition.objects.filter(action_numb=1,revision = rule.dynamicforms.revision)
		leads_condition = WorkFlow.objects.filter(action_numb=2)
		return render(request,'workflow/workflow-rules.html',locals())
	return render(request,'workflow/workflow.html',locals())

def workFlowSave(request,id):
	school = Profile.objects.get(user_id = request.user)
	if request.method == "POST":
		createrule = CreateRule.objects.get(id=id)
		workflowwhen = WorkFlowWhen.objects.create(
			when = request.POST['record_action'],
			createrule_id = createrule.id,
			)
		for index,j in enumerate(request.POST.getlist('leads_action[]')):
			workflowleads = WorkFlowLeads.objects.create(
				workflowwhen_id = workflowwhen.id,
				leads = request.POST.getlist('leads_action[]')[index],
				condition_arthimatic = request.POST.getlist('leads_condition[]')[index],
				condition = request.POST.getlist('condition[]')[index],
				)
		return HttpResponseRedirect('/workflow/workflowsave/'+str(id))
	rule = CreateRule.objects.get(id = id)
	recordaction = WorkFlow.objects.filter(action_numb=1)
	score = WorkFlow.objects.filter(action_numb=2)
	leads = WorkFlowCondition.objects.filter(action_numb=1,revision = rule.dynamicforms.revision)
	when = WorkFlowWhen.objects.get(createrule = id)
	when_leads = WorkFlowLeads.objects.raw('SELECT `workflow_workflowleads`.`id`, `workflow_workflowleads`.`leads`, `workflow_workflowleads`.`condition_arthimatic`, `workflow_workflowleads`.`condition`, `workflow_workflowleads`.`created_on`,`workflow_workflowcondition`.`actions` FROM `workflow_workflowleads` INNER JOIN `workflow_workflowcondition` ON (`workflow_workflowcondition`.`name` = `workflow_workflowleads`.`leads`) WHERE `workflow_workflowleads`.`workflowwhen_id` = %s' %when.id)
	leads_condition = WorkFlow.objects.filter(action_numb=2)
	template = EmailTemplate.objects.filter(school=school)
	instant_actions = EmailNotification.objects.filter(create_rule = id).first()
	schedule_actions = EmailScheduleReport.objects.filter(create_rule = id).first()
	return render(request,'workflow/workflow-rules-update.html',locals())



def emailNotification(request,id):
	rule = CreateRule.objects.get(id = id)
	if request.method == 'POST':
		email = EmailNotification.objects.filter(create_rule = id)	
		# return HttpResponse(email)	
		if not email:
			emailnotification = EmailNotification.objects.create(name=request.POST['name'],
				email_recipients = request.user,
				additional_recipients = request.POST['aditional_receipent'],email_template_id = request.POST['email_template'],create_rule=rule,
				send_as = request.POST['send_as'])
		else:
			email.update(name=request.POST['name'],
				additional_recipients = request.POST['aditional_receipent'],email_template_id = request.POST['email_template'],
				send_as = request.POST['send_as'])
		return HttpResponseRedirect('/workflow/workflowsave/'+str(id))



def emailSchedule(request,id):
	create_rule = CreateRule.objects.filter(id=id)
	if request.method == 'POST':
		# time_value = request.POST['num_of_time']
		time_hr_value = request.POST['hr_day_value']
		unit_value = request.POST['time_unit']
		if unit_value == 'Hours':
			time_in_min = int(time_hr_value) * int(60)
		if unit_value == 'Days':
			time_in_min = int(time_hr_value) * int(1440)
		if unit_value == 'Minutes':
			time_in_min = time_hr_value 

		s = EmailScheduleReport.objects.create(
			name = 'Scheduled Email',
			create_rule_id = id,
			email_template_id = request.POST['email_template'],
			time_in_minute = time_in_min,
			time = time_hr_value,
			time_unit = unit_value,
		)
		s.save()
	return HttpResponseRedirect('/workflow/workflowsave/'+str(id))
# def test(request):
# 	createrule = CreateRule.objects.all()
# 	return HttpResponse(createrule[0].dynamicforms.school_id.school)

def createTemplate(request):
	school = Profile.objects.get(user_id = request.user)
	module = DynamicForms.objects.filter(school_id = school)
	if request.method == 'POST':
		EmailTemplate.objects.create(template_name=request.POST['template'],subject=request.POST['subject'],
			content=request.POST['content'],module_name_id=request.POST['module'],school_id=school.id)
	return render(request,'workflow/template.html',locals())

def whenUpdate(request,id):
	if request.method == 'POST':
		workflowwhen = WorkFlowWhen.objects.filter(createrule_id=id).update(
			when = request.POST['record_action'],
			)
	return HttpResponseRedirect('/workflow/workflowsave/'+str(id))

def conditionEdit(request,id,rule_id):
	rule = CreateRule.objects.get(id = rule_id)
	wrkflw_lead = WorkFlowLeads.objects.get(id = id)
	leads = WorkFlowCondition.objects.filter(action_numb=1,revision = rule.dynamicforms.revision)
	leads_condition = WorkFlow.objects.filter(action_numb=2)
	return render(request,'workflow/condition-edit.html',locals())

def conditionUpdate(request,id,rule_id):
	if request.method == 'POST':
		WorkFlowLeads.objects.filter(id = id).update(leads = request.POST.get('leads_action'),
				condition_arthimatic = request.POST.get('leads_condition'),
				condition = request.POST.get('condition'),)
	return HttpResponseRedirect('/workflow/workflowsave/'+str(rule_id))


def newWorkflowConditoin(request,id):
	if request.method == 'POST':
		when = WorkFlowWhen.objects.get(createrule = id)
		for index,j in enumerate(request.POST.getlist('leads_action[]')):
			workflowleads = WorkFlowLeads.objects.create(
				workflowwhen_id = when.id,
				leads = request.POST.getlist('leads_action[]')[index],
				condition_arthimatic = request.POST.getlist('leads_condition[]')[index],
				condition = request.POST.getlist('condition[]')[index],
				)
	return HttpResponseRedirect('/workflow/workflowsave/'+str(id))

def conditionDelete(request,id,rule_id):
	delete_wrkleads = WorkFlowLeads.objects.get(id=id)
	delete_wrkleads.delete()
	return HttpResponseRedirect('/workflow/workflowsave/'+str(rule_id))

