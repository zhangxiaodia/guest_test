from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest

# Create your views here.

def index(request):
	return render(request,"index.html")
def login_action(request):
	if request.method=='POST':
		username=request.POST.get('username','')
		password=request.POST.get('password','')
		user=auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request,user)
		#if username=="admin" and password=="admin123":
			response=HttpResponseRedirect('/event_manage/')
			request.session["user"]=username;
			response.set_cookie("user",username,3600)
			return response
		else:
			return render(request,"index.html",{"error":"username or password error"})
@login_required
def event_manage(request):
	#username=request.COOKIES.get("user","")
	event_list=Event.objects.all()
	username=request.session.get("user","")
	return render(request,"event_manage.html",{"user":username,"events":event_list})
@login_required
def search_name(request):
	username=request.session.get("user","")
	search_name=request.GET.get("name","")
	event_list=Event.objects.filter(name__contains=search_name)
	return render(request,"event_manage.html",{"user":username,"events":event_list})
@login_required
def search_realname(request):
	username=request.session.get("user","")
	search_realname=request.GET.get("realname","")
	guest_list=Guest.objects.filter(name__contains=search_realname)
	return render(request,"guest_manage.html",{"user":username,"guests":guest_list})
@login_required
def guest_manage(request):
	guest_list=Guest.objects.all()
	username=request.session.get("user","")
	return render(request,"guest_manage.html",{"user":username,"guests":guest_list})

@login_required
def sign_index(request,eid):
	event=get_object_or_404(Event,id=eid)
	return render(request,"sign_index.html",{"event":event})
@login_required
def sign_index_action(request,eid):
	event=get_object_or_404(Event,id=eid)
	phone =request.POST.get("phone","")
	print(phone)
	result=Guest.objects.filter(phone=phone)
	if not result:
		return render(request,"sign_index.html",{"event":event,'hint':'phone wrong'})

@login_required
def loginout(request):
	auth.logout(request)
	response=HttpResponseRedirect('/index/')
	return response