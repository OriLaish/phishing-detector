from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def main(requst):
    print(requst.GET.get('url'))
    return HttpResponse("Hello")
