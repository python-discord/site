from django.shortcuts import render
from django.http import HttpResponse


def hello(_request):
    return HttpResponse("Hi!")