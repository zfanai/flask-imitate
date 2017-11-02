#encoding:utf8

import json
import urllib2,urllib

context={}

def http_post(req_url, args, **opt):
    show_header=opt.get('show_header', False)
    pass
    #data = urllib.urlencode({
    #    'flag': 'apply_monitor', 'user_name': 'test15'
    #})
    if args:
        data = urllib.urlencode(args)
    else:
        data=None
    req = urllib2.Request(req_url, data, {'Cookie':context.get('cookie')})
    rsp = urllib2.urlopen(req)
    rv = rsp.read()
    if show_header:
        print 'header:', rsp.headers
    return rv

if __name__=='__main__':
    http_post('http://127.0.0.1:5000/index2', None, show_header=True)