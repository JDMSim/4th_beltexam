from django.shortcuts import render, redirect
from ..loginRegistration_app.models import User
from .models import  Quote
from django.contrib  import messages

def index(request):
    quotes =  Quote.objects.all().exclude(likes__id = request.session['user_id'])
    fav_quotes = Quote.objects.filter(likes__id = request.session['user_id'])
    context = {'quotes':quotes, 'fav_quotes':fav_quotes}
    return render(request, 'belt_exam_app/index.html', context)

def create(request):
    response = Quote.objects.create_qt(request.POST, request.session['user_id'])
    if response['status']:
        return redirect('beltexam:home')
    else:
        for error in response['errors']:
            messages.error(request, error)
        return redirect('beltexam:home')

def add(request, id):
    Quote.objects.add(id, request.session['user_id'])
    return redirect('beltexam:home')

def remove(request, id):
    Quote.objects.remove(id, request.session['user_id'])
    return redirect('beltexam:home')

def user(request, id):
    usr_qt = Quote.objects.filter(creator__id = id)
    print usr_qt[0].creator.first_name
    context = {'quotes':usr_qt}
    return render(request, 'belt_exam_app/user.html', context)
# Create your views here.
