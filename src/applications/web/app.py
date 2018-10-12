from src.lib.application.webApp.webApp import WebApp as BaseWebApp
from src.applications.web.env.Development import Development

class WebApp(BaseWebApp):
    
    def isDevelopment(self):
        return type(self.getEnv()) == Development
    
    def getRoutes(self):
        return self.getEnv().getConfig()['web-app']['routes']
