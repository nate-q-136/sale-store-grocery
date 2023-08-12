from django.shortcuts import render
from django.http import HttpResponse
from userauths.models import User
# Create your views here.
def index(request):
    context = {
        'user':None
    }
    return render(request, 'core/index.html',context)
    # return HttpResponse("welcome to my shop")
    pass
