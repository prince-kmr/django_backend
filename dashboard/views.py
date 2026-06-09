from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# def home(request):
#     return HttpResponse("Hello world")

# def courseDetails(request, courseid):
#     return HttpResponse(courseid)


# def home(request):
#     context = {
#         "title": "My Website",
#         "heading": "Welcome to Django",
#         "items": ["Python", "Django", "React"]
#     }

#     return render(request, "dashboard/index.html", context)


from django.shortcuts import render
import random

def dynamic_home(request):
    # This is the dynamic data we want to send to the HTML
    context = {
        'username': 'CoderExtraordinaire',
        'lucky_numbers': [random.randint(1, 100) for _ in range(3)]
    }
    
    # Render takes: request, the path to the template, and the data (context)
    return render(request, 'dashboard/index.html', context)