# -*- coding:utf-8 -*-

from ipx import *
from datetime import datetime,timedelta


def user_agent( data):
    if type(data) is list:
        return [ user_agent(i) for i in data ]

    device_pc = {
        'windows nt':'Windows',
        'mac':'Mac OS',
        'linux':'Linux',
        'unix':'Unix',
        'sunos':'Unix',
        'bsd':'Unix'
    }

    device_mobi = {
    'android':'Android',
    'iphone':'iPhone',
    'ipad':'iPad',
    'AppleWebKit': 'iPhone'
    }

    for key in device_mobi.keys():
        if  device_mobi[key] in data:
            return device_mobi[key], True


    for key in device_pc.keys():
        if  device_pc[key] in data:
            return device_pc[key], False


    return 'UNKONW',None


def ip( data):
    IP.load(os.path.abspath("conse/17monipdb.dat"))
    def _ip(data):
        return [i.strip() for i in IP.find(data).strip().split('\t')]

    if type( data) is list:
        return [ _ip(i) for i in data ]
    return _ip(data)


def stand_time( data):
    if type(data) is list:
        return [user_agent(i) for i in data]

    ret = datetime.strptime(data[:-6],'%d/%b/%Y:%H:%M:%S')
    if data[-5]=='+':
        ret-= timedelta(hours=int(data[-4:-2]),minutes=int(data[-2:]))
    elif data[-5]=='-':
        ret+= timedelta(hours=int(data[-4:-2]),minutes=int(data[-2:]))
    return ret


def url_parser(data):

    _split_ = lambda x,y: filter(lambda e:e, x.split(y))

    data = _split_(data, '?')

    temp = _split_(data[0], '://')

    accessType = temp.pop(0) if len(temp) is 2 else None

    path =filter( lambda x: x != 'https:' and x !=  'http:',  _split_(temp.pop(0), '/'))

    param = {}


    if len(data) is 2:
        for p in  _split_(data[1],'&'):
            p = _split_(p,'=')
            param[p[0]] =  p[1] if len(p) is 2 else None
    return path, param, accessType


def request_parser(data):
    data = data.strip().split(' ')
    if len(data) == 3:
        path, param, temp = url_parser(data[1])
        return data[0], path, param, data[2]
    return 0

