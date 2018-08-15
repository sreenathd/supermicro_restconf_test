import requests
import os
import json

class RestCalls():

    def __init__(self, ip_address, port=80, username=None, password=None):
        self.BasePath = '/restconf/data/running/openconfig-'
        #self.BasePath = ''
        self.Accept = [
            'application/yang.data+json',
            'application/yang.errors+json',
        ]
        self.ContentType = 'application/yang.data+json'
        session = requests.Session()
        self.Format = 'json'
        if username is not None and password is not None:
            session.auth = (username, password)
        session.verify = False
        session.headers.update({
            'Accept': ','.join([
                accept.format(fmt=self.Format) for accept in self.Accept
            ]),
            'Content-Type': self.ContentType.format(fmt=self.Format),
        })
        self._session = session
        self._host = '{scheme}://{ip}:{port}{basePath}'.format(
            scheme='http',
            ip=ip_address,
            port=port,
            basePath=self.BasePath
        )

    def put(self, data, endpoint):
        url = self._host + endpoint
        print(url)
        res = self._session.put(url, data=data)
        return res

    def post(self, data, endpoint):
        url = self._host + endpoint
        print(url)
        res = self._session.post(url, data=data)
        return res

    def patch(self, data, endpoint):
        url = self._host + endpoint
        print(url)
        res = self._session.patch(url, data=data)
        return res

    def get(self, endpoint='', **kwargs):
        url = self._host + endpoint
        print(url)
        if 'content' not in kwargs:
            kwargs = {'content': 'config'}
        print(url)
        res = self._session.get(url, params=kwargs)
        return res

    def delete(self, endpoint):
        url = self._host + endpoint
        print(url)
        res = self._session.delete(url)
        return res
    
def update_conf():
    ip = os.environ.get('SWITCH_IP')
    print(ip)
    port = os.environ.get('SWITCH_PORT')
    print(port)
    user = os.environ.get('REST_USER')
    print(user)
    pswd = os.environ.get('REST_PSWD')
    print(pswd)
    return [ip,port,user,pswd]
    
def get(uri=''):
    resp = update_conf()
    rest_session = RestCalls(resp[0],resp[1],resp[2],resp[3])
    resp = rest_session.get(uri)
    return resp

def delete(uri=''):
    resp = update_conf()
    rest_session = RestCalls(resp[0],resp[1],resp[2],resp[3])
    resp = rest_session.delete(uri)
    return resp

def post(uri='',data=None):
    #data = json.loads(data)
    resp = update_conf()
    rest_session = RestCalls(resp[0],resp[1],resp[2],resp[3])
    resp = rest_session.post(data,uri)
    return resp

def put(uri='',data=None):
    #data = json.loads(data)
    resp = update_conf()
    rest_session = RestCalls(resp[0],resp[1],resp[2],resp[3])
    resp = rest_session.put(data,uri)
    return resp

def patch(uri='',data=None):
    #data = json.loads(data)
    resp = update_conf()
    rest_session = RestCalls(resp[0],resp[1],resp[2],resp[3])
    resp = rest_session.patch(data,uri)
    return resp

