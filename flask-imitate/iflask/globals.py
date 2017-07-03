#encoding:utf8

from werkzeug.local import LocalStack


_request_ctx_stack=LocalStack()