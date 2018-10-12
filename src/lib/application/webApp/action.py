import tornado.web


class Action(tornado.web.RequestHandler):
    _di = None
    _env = None
    _args = None
    _kwargs = None
    
    def getDi(self):
        return self._di
    
    def getEnv(self):
        return self._env
    
    def getArgs(self):
        return self._args
    
    def getKwargs(self):
        return self._kwargs
    
    def setDi(self, di):
        self._di = di
    
    def setEnv(self, env):
        self._env = env
    
    def setArgs(self, args):
        self._args = args
    
    def setKwargs(self, kwargs):
        self._kwargs = kwargs
    
    def initialize(self, env, di, args, **kwargs):
        self.setEnv(env)
        self.setDi(di)
        self.setArgs(args)
        self.setKwargs(kwargs)