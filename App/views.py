from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from urllib.parse import urlparse
from datetime import datetime, timedelta
from .db import save_data
from functools import wraps

# Create your views here.

def cors(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        response = f(*args,**kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    return wrapper

@csrf_exempt
@cors
@require_http_methods('POST')
def receiver(request):

    if('result' in request.POST):
        dataset = json.loads(request.POST['result'])
        if dataset:
            ip = get_client_ip(request)
            value = ''
            for data in dataset:
                query = data[0]
                domain = get_host(query)
                response_time = data[1]
                date = datetime.fromtimestamp(data[2]/1000) + timedelta(hours=8)
                date = date.strftime('%Y-%m-%d %H:%M:%S')
                value += '("%s", "%s", "%s", %s, "%s"),' % (ip, domain, query, response_time, date)

            value = value[:-1]
            print(value)
            year_month = datetime.now().strftime('%Y%m')
            save_data(year_month, value)
    return HttpResponse()

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_host(url):

    return urlparse(url).netloc

def test(request):
    # a = test_db()
    # print(a)
    return HttpResponse('TEST')
