import requests
import urllib3
from requests import Session, Response
import json

import duosession

class DuoRequest(object):
    
    def do_request(url, duoSession, data=None, method=None) -> Response:
        
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}
        if duoSession.jwt is not None:
            headers['Authorization'] = 'Bearer ' + duoSession.jwt

        req = requests.Request(method if method else ('POST' if data else 'GET'),
                               url,
                               data=json.dumps(data),
                               headers=headers,
                               cookies=duoSession.session.cookies)
        print(url)
        prepped = req.prepare()
        response = duoSession.session.send(prepped)
        return response
