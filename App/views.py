from django.core.validators import validate_ipv4_address
from django.http import HttpResponse, RawPostDataException
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from urllib.parse import urlparse
from datetime import datetime, timedelta
from .db import save_data
from functools import wraps
from .token import Token

# Create your views here.


def cors(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        response = f(*args,**kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    return wrapper

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


@csrf_exempt
@cors
@require_http_methods('POST')
def receiver_token(request, theToken):
    token = Token(theToken)
    try:
        token_info = token.decode()
        receiver(request, token_info[0], token_info[1])
        return HttpResponse()
    except KeyError:
        print("No Token Exist - " + theToken)


def test(request):

    return HttpResponse('OK')

def receiver(request, user, device):
    ip = get_client_ip(request)
    validate_ipv4_address(ip)
    user_agent = request.headers['User-Agent']
    # exit()
    # print(request.POST)
    # print(request.body)
    dataset = json.loads(request.body)
    print(ip)
    print(user_agent)
    print(dataset)
    # return HttpResponse()
    value = ''
    for data in dataset:
        # print(data)
        query = data
        domain = urlparse(query).hostname
        # print(dataset[data]['datetime'])
        timestamp = datetime.fromtimestamp(int(dataset[data]['datetime'])/1000)+timedelta(hours=8)
        timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        response_time = int(dataset[data]['response'])

        # print(domain, query, timestamp, response_time)
        domain = ''
        if domain:
            value += '("%s", "%s", "%s", %s, "%s", %s, "%s"),' % (ip, domain, query, response_time, device, "%(user-agent)s", timestamp)
        else:
            print("invalid url:", domain)
            raise Exception("invalid url:", domain)
    value = value[:-1]
    year_month = datetime.now() + timedelta(hours=8)
    year_month = year_month.strftime('%Y%m')
    table_name = 'sdk_report_%s_%s' % (user, year_month)
    save_data(table_name, value, user_agent)

def token_generator(request):
    return HttpResponse(Token.generator())
