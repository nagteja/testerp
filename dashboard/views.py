from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

def dashboard(request):
	return render(request,'dashboard/index.html')
