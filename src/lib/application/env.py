class Env(object):
    _config = {}
    _parent = None
    BASE_PATH = None
    
    def getConfig(self):
        return self._config
    
    def setConfig(self, config = {}):
        self._config = config
    
    def mergeConfig(self, a: {}, b: {}):
        z = {}
        for x in a:
            for y in b:
                if (x == y) and type(a[x]) == dict and type(b[y]) == dict:
                    z[x] = self.mergeConfig(a[x], b[y])
        
        c = {**a, **b, **z}
        return c
    
    def getParent(self):
        return self._parent
    
    def setParent(self, parent):
        self._parent = parent
