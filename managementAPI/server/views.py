from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.
class MenuItems(View):
    def get(self, request):
        return HttpResponse("<h1>STATUS 200 OK</h1>")
    
    def post(self, request):
        return HttpResponse("<h1>STATUS 403 UNAUTHORIZED</h1>")
