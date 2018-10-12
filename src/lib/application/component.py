class Component(object):
    _env = None
    _di = None
    _args = None
    _kwargs = None
    
    def setDi(self, di):
        self._di = di
    
    def getDi(self):
        return self._di
    
    def getEnv(self):
        return self._env
    
    def setEnv(self, env):
        self._env = env
    
    def setArgs(self, args):
        self._args = args
    
    def getArgs(self):
        return self._args
    
    def setKwargs(self,kwargs):
        self._kwargs = kwargs
        
    def getKwargs(self):
        return self._kwargs
    
    def __init__(self, env, di, args, **kwargs):
        self._env = env
        self._di = di
        self._args = args
        self._kwargs = kwargs
    
    def run(self):
        raise Exception("implement run in {0}".format(self))
