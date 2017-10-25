from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'belt_exam/index.html')

def login(request):
    if request.method == 'POST':
        if not 'login_status' in request.session:
            request.session['login_status'] = False
        login_data = User.objects.filter(username=request.POST['username'])
        inputted_password = request.POST['password']
        stored_password = User.objects.filter(username=request.POST['username']).first().password
        if login_data and bcrypt.checkpw(inputted_password.encode(), stored_password.encode()):
            request.session['login_status'] = {'id':login_data.first().id, 'name':login_data.first().name, 'username':login_data.first().username}
            print request.session['login_status']
            return redirect('/belt_exam')
        else:
            messages.error(request, "Email and password does not match")
            return redirect('/')

def logout(request):
    request.session['login_status'] = False
    return redirect('/')

def add_user(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for error in errors.itervalues():
                messages.error(request, error)
            return redirect('/')
        else:
            password = request.POST['password']
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hashed_password)
            messages.error(request, "Registered!")
            return redirect('/')

def belt_exam(request):
    quotes = Quote.objects.all()
    this_quote = Quote.objects.all()
    context = {
        'quotes':quotes,
        'this_quote': this_quote
    }
    return render(request, 'belt_exam/quote_list.html', context)

def add(request):
    if request.method == 'POST':
        this_user = User.objects.get(id=request.session['login_status']['id'])
        temp = Quote.objects.create(
            quotename=request.POST['quote_name'], 
            added_by=this_user)
        temp.quoted_by.add(this_user)
    return redirect('/belt_exam')

def add_to_quotelist(request):
    if request.method == 'POST':
        this_user = User.objects.get(id=request.session['login_status']['id'])
        this_quote = Quote.objects.get(id=request.POST['quote_id'])
        this_quote.quoted_by.add(this_user)
    return redirect('/belt_exam')

def remove_quote(request):
    if request.method == 'POST':
        this_user = User.objects.get(id=request.session['login_status']['id'])
        this_quote = Quote.objects.get(id=request.POST['quote_id'])
        this_quote.quoted_by.remove(this_user)
    return redirect('/belt_exam')

def quote_detail(request, quote_id):
    quote_all = Quote.objects.all()
    context = {
        'quote':quote_all
    }
    return render(request, 'belt_exam/quote_detail.html', context)