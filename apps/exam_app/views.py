from django.shortcuts import render, redirect, HttpResponse 
from django.contrib import messages
from .models import User, Trip
import bcrypt
from datetime import datetime

def index(request):
    return render(request, "exam_app/index.html")

def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags="register_error")
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            request.session['first_name'] = request.POST['first_name']
            request.session['email'] = request.POST['email']
            User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
            email_address=request.POST['email'], birthday=request.POST['birthday'], password=pw_hash)
            return redirect('/dashboard')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="login_error")
        return redirect('/')
    else:
        user = User.objects.filter(email_address=request.POST['login_email'])
        logged_user = user[0]
        request.session['first_name'] = logged_user.first_name
        request.session['email'] = logged_user.email_address
        return redirect('/dashboard')

def dashboard(request):
    if "email" in request.session:
        this_user = User.objects.get(email_address=request.session['email'])
        context = {
            "your_trips": this_user.trips_join.all(),
            "other_trips": Trip.objects.exclude(users_join=this_user)
        }
        return render(request, "exam_app/dashboard.html", context)
    else: 
        return HttpResponse("Please go back to log in or register first! Thank you!")

def remove(request, num):
    this_trip=Trip.objects.get(id=num)
    if this_trip.users_created.email_address == request.session['email']:
        this_trip.delete()
        return redirect('/dashboard')
    else:
        return redirect('/dashboard')

def edit(request,num):
    if "email" in request.session:
        this_trip=Trip.objects.get(id=num)
        if this_trip.users_created.email_address == request.session['email']:
            context = {
                "id":this_trip.id,
                "destination": this_trip.destination,
                "start_date": this_trip.start_date.strftime("%Y-%m-%d"),
                "end_date": this_trip.end_date.strftime("%Y-%m-%d"),
                "plan": this_trip.plan,
            }
            return render(request, "exam_app/edit.html", context)
        else:
            return redirect('/dashboard')
    else:
        return HttpResponse("Please go back to log in or register first! Thank you!")

def trip_update(request,num):
    this_trip=Trip.objects.get(id=num)
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/edit/' + num)
    else: 
        this_trip.destination=request.POST['destination']
        this_trip.start_date=request.POST['start_date']
        this_trip.end_date=request.POST['end_date']
        this_trip.plan=request.POST['plan']
        this_trip.save()
        return redirect('/dashboard')

def join(request,num):
    this_user = User.objects.get(email_address=request.session['email'])
    this_trip=Trip.objects.get(id=num)
    this_user.trips_join.add(this_trip)
    return redirect('/dashboard')

def move_to_bottom(request,num):
    this_user = User.objects.get(email_address=request.session['email'])
    this_trip=Trip.objects.get(id=num)
    this_user.trips_join.remove(this_trip)
    return redirect('/dashboard')

def new_trip(request):
    if "email" in request.session:
        return render(request, "exam_app/new_trip.html")
    else:
        return HttpResponse("Please go back to log in or register first! Thank you!")

def trip_create(request):
    this_user = User.objects.get(email_address=request.session['email'])
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/new')
    else: 
        this_trip = Trip.objects.create(destination=request.POST['destination'],start_date=request.POST['start_date'],
        end_date=request.POST['end_date'],plan=request.POST['plan'],users_created=this_user)
        this_trip.save()
        this_trip.users_join.add(this_user)
        return redirect('/dashboard')

def cancel(request):
    return redirect('/dashboard')

def one_trip(request,num):
    if "email" in request.session:
        this_trip=Trip.objects.get(id=num)
        this_user = User.objects.get(email_address=request.session['email'])
        context = {
            "destination": this_trip.destination,
            "start_date":this_trip.start_date.strftime("%m/%d/%y"),
            "end_date":this_trip.end_date.strftime("%m/%d/%y"),
            "created_at":this_trip.created_at.strftime("%m/%d/%y"),
            "updated_at":this_trip.updated_at.strftime("%m/%d/%y"),
            "plan":this_trip.plan,
            "user_create":this_trip.users_created.id,
            "users_created":this_trip.users_created.first_name + " " + this_trip.users_created.last_name,
            "users_join": this_trip.users_join.all(),
        }
        return render(request, "exam_app/one_trip.html", context)
    else:
        return HttpResponse("Please go back to log in or register first! Thank you!")

def go_back(request):
    return redirect('/dashboard')

def logout(request):
    del request.session['first_name']
    del request.session['email']
    return redirect('/')