from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, AddRecordForm
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from .models import Record
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import RecordSerializer
from rest_framework import permissions
from django.core.cache import cache

# Create your views here.
def home(request):
	record_cache = cache.get("record_cache")
	if record_cache:
		records = record_cache
	else:
		records = Record.objects.all()
		cache.set("record_cache", records, 60)
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user=user)
			messages.success(request, "You have been logged in!")
			return redirect('website:home')
		else:
			messages.success(request, "There was an error logged in please try again")
			return redirect('website:home')

	else:
		return render(request, 'home.html', {"records": records})

# def login_user(request):
# 	pass

def logout_user(request):
	logout(request)
	messages.success(request, "You have been logged out")
	return redirect('website:home')


def register_user(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password1"]
			user = authenticate(username=username, password=password)
			login(request, user=user)
			messages.success(request, "You have successfully rigets")
			return redirect("website:home")
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})
	return render(request, 'register.html', {'form':form})


def customer_record(request, pk):
	if request.user.is_authenticated:
		# customer_record_cache = cache.get("customer_record")
		# if customer_record_cache:
		# 	customer_record = customer_record_cache
		# else:
		# 	customer_record = Record.objects.get(id=pk)
		# 	cache.set("customer_record", customer_record, 60)
		
		customer_record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		messages.success(request, "You must be looged in to view that page")
		return redirect('website:home')


def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = Record.objects.get(id=pk)
		delete_it.delete()

		cache.delete("record_cache")

		messages.success(request, "Record Deleted successfully")
		return redirect('website:home')
	else:
		messages.success(request, "You must be looged in to do that")
		return redirect('website:home')


def add_record(request:HttpRequest):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save()

				cache.delete("record_cache")

				messages.success(request, "Record Added")
				return redirect('website:home')
			else:
				return HttpResponseBadRequest("Incorrect data")
		return render(request, 'add_record.html', {"form":form})
	else:
		messages.success(request, "You must be Logged in ")
		return redirect('website:home')


def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()

			cache.delete("record_cache")

			messages.success(request, "Record has been updated! ")
			return redirect('website:home')
		return render(request, 'update_record.html', {"form":form})
	else:
		messages.success(request, "You must be Logged in ")
		return redirect('website:home')
	
class GetRecordListView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request:HttpRequest):
		queryset = Record.objects.all()
		serializer_for_queryset = RecordSerializer(
			instance=queryset,
			many=True
		)
		return Response(serializer_for_queryset.data)
	
class GerRecordDetailView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request:HttpRequest, pk:int):
		queryset = Record.objects.get(id=pk)
		serializer_for_queryset = RecordSerializer(
			instance=queryset
		)
		return Response(serializer_for_queryset.data)