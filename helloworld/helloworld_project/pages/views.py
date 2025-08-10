from django.shortcuts import render
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("¡Hola, Valentina! Esta es mi primera vista en Django.")
