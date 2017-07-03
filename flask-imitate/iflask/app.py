#encoding:utf8

from .wrappers import Response, Request
from .ctx import RequestContext
from .globals import _request_ctx_stack
from werkzeug.routing import Rule, Map

# 170628, Flask是一个遵循WSGI标准的应用, 所以Flask必须是可调用的。也就是定义__call__属性
# bytes类型和str类型是同一个类型。 bytearray跟bytes很像, 只是类型不一样， 然后可以指定长度生成一个buffer
# 重点研究怎么返回响应数据的，为什么是通过迭代对象的方式来返回响应数据。具体怎么通过迭代对象的方式返回数据，flask app和werkzueg之间的接口
# 有哪些。
# 起始很多底层的功能还是有werkzeug来完成的。
# 用回调， 设置回调函数， 回调对象。
# 2017-6-29 
#  1. 增加route函数， 可以映射由和处理函数。
#  2. 下一步要增加全局的上下文功能， 
class Flask(object):
    
    response_class=Response
    request_class=Request
    view_functions={}
    url_rule_class=Rule
    url_map=Map()
    
    def run(self):
        print 'Flask.run'
        from werkzeug.serving import run_simple
        run_simple('127.0.0.1', 5000, self, use_reloader=True)
    
    def route(self, rule, **options):
        def decorator(f):
            print 'route:', rule
            self.add_url_rule(rule, view_func=f, **options)        
            return f
        return decorator
    
    def create_url_adapter(self, request):
        return self.url_map.bind_to_environ(request.environ)
    
    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        print 'add_url_rule'
        if not endpoint:
            endpoint=view_func.__name__
            print 'view_func.name:', endpoint
        #
        rule=self.url_rule_class(rule, methods=['GET'], endpoint=endpoint)
        self.url_map.add(rule)
        print 'rule:', rule, type(rule)
        #
        self.view_functions[endpoint]=view_func
    
    def make_response(self, rv):
        #rv=self.response_class(('dfdd', '\n'))
        rv=self.response_class(rv)
        return rv
    
    def dispatch_request(self):
        #self.view_functions[]
        #return ('df', '+', 'ddd')
        req=_request_ctx_stack.top.request
        rule=req.url_rule
        print 'rule:', rule, rule.endpoint
        #for k in dir(req):print 'req:', k
        return self.view_functions[rule.endpoint](**req.view_args)
        #return ['df', '+', 'ddd']
    
    def full_dispatch_request(self):
        rv=self.dispatch_request()
        response=self.make_response(rv)
        return response
    
    def request_context(self, environ):
        #for k in environ:print 'environ:', k
        return RequestContext(self, environ)
    
    def wsgi_app(self, environ, start_response):
        # 
        #for k,v in environ.items():print 'env:', k, v
        # 在app处理的最前面就就开始构建请求的上下信息。 
        ctx=self.request_context(environ)
        ctx.push()
        
        try:    
            #response=self.make_response(['a', 'dfef'])
            response=self.full_dispatch_request()
            print 'response:', response, type(response)
            #for i in response:
            #    print 'response:', i
            
            # 响应类是可以调用的， 调用的结果是返回一个可以迭代的对象
            rv=response(environ, start_response)
            # 如果在这里迭代了， 就相当于用完了，不会像list那样可以重新迭代， list的迭代起始是每次迭代的时候都创建一个新的迭代器
            #for d in rv:
            #    print 'd:', d
            return rv
        # finally在return之前也会调用。  
        finally:
            print 'wsgi_app,finally.'
        
    def __call__(self, environ, start_response):
        #print 'Flask.__call__:', environ, start_response
        return self.wsgi_app(environ, start_response)