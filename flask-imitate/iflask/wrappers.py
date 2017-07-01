#encoding:utf8

from werkzeug.wrappers import Response as ResponseBase, Request as RequestBase


class Request(RequestBase):
    pass

class Response(ResponseBase):
    default_mimetype='text/html'