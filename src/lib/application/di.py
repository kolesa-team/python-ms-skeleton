class Di(object):
    _env = None
    _args = None
    
    def getEnv(self):
        return self._env
    
    def setEnv(self, env):
        self._env = env
    
    def setArgs(self, args):
        self._args = args
    
    def getArgs(self):
        return self._args
    
    def __init__(self, env, args):
        self._env = env
        self._args = args