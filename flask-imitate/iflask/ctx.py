#encoding:utf8

from .globals import _request_ctx_stack

# 请求的上下文， 包括app, g, request等对象
class RequestContext(object):
    def __init__(self, app, environ, request=None):
        self.app=app  # current_app
        if not request:
            request=self.app.request_class(environ)
        self.request=request
        self.url_adapter=app.create_url_adapter(self.request)
        
        self.match_request()
    
    def match_request(self):
        print 'adp:', self.url_adapter
        url_rule,self.request.view_args=self.url_adapter.match(return_rule=True)
        self.request.url_rule=url_rule
    
    def push(self):
        print 'request ctx push'
        # 保存线程本地化的请求上下文
        # 在实际的flask源码中， 还要保存App的上下文信息和处理会话的信息。
        _request_ctx_stack.push(self)
        