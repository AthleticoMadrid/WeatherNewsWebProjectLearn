from urllib.parse import urlparse, urljoin
from flask import request

def is_safe_url(target):
    ref_url = urlparse(request.host_url)                        #берём ссылку нашего сайта
    test_url = urlparse(urljoin(request.host_url, target))      #сравнить что отправляем пользователя на верный url
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in request.values.get('next'), request.referrer:         #если в строке адреса передан параметр 'next'
        if not target:
            continue
        if is_safe_url(target):
            return target