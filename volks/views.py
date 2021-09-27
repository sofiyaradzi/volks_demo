from django.shortcuts import render


def home(request):
    return render(request, 'volks/volks_home.html')
