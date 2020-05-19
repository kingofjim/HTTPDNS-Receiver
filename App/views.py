from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .db import *
from .red import submit_node_testing

from functools import wraps

# Create your views here.

# @require_http_methods(['GET','POST'])

def cors(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        response = f(*args,**kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    return wrapper


@csrf_exempt
@cors
# @require_http_methods('POST')
def receiver(request):
    data = json.loads(request.POST['result'])
    print(data)

    # sorting
    # data.sort(key=lambda e: e[3])
    # print(data)

    response = HttpResponse()
    submit_node_testing(data)
    return response

def test(request):
    a = test_db()
    print(a)
    return HttpResponse('TEST')
