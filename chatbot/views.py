from django.shortcuts import render
import data_parsing
# Create your views here.


def home(request):
    context = {}

    return render(request, "chathome.html", context)

def professor_info(request):
