#encoding:utf8

from iflask import Flask

def create_app():
    app=Flask()
    @app.route('/')
    def index():
        return 'hello'
    @app.route('/index2')
    def index2():
        return 'hello2'
    
    return app 