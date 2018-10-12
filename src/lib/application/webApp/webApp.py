import tornado.ioloop
import tornado.web

from src.lib.application.baseApp import BaseApp


class WebApp(BaseApp):
    
    def getRoutes(self):
        raise Exception("implement method getRoutes in {0}".format(self))
    
    def _processRoutes(self, routes):
        result = []
        
        for route in routes:
            result.append(
                (
                    r"{0}".format(routes[route]['url']),
                    routes[route]['action'],
                    dict(env = self.getEnv(), di = self.getDi(), args = self.getArgs(), **routes[route]['kwargs'])
                )
            )
        
        return result
    
    def make_app(self):
        
        applicationRoutes = self._processRoutes(self.getRoutes())
        
        autoreload = False
        
        if self.isDevelopment():
            autoreload = True
        
        return tornado.web.Application(applicationRoutes, autoreload=autoreload)
    
    def listen_message(self, host, port):
        print("running web application on {}:{}", host, port)
        
    def isDevelopment(self):
        raise Exception('implement method isDevelopment')
    
    def run(self):
        app = self.make_app()
        port = self.getEnv().getConfig()['web-app']['port']
        host = self.getEnv().getConfig()['web-app']['host']
        
        self.listen_message(host, port)
        app.listen(port, host)
        
        tornado.ioloop.IOLoop.current().start()
