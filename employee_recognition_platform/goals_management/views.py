from django.shortcuts import render

def index(request):
    return render(request, 'goals_management/index.html')
