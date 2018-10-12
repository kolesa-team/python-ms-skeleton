import json
import requests

from src.lib.application.component import Component


class HttpClient(Component):
    _method = "GET"
    _scheme = "http"
    _port = 80
    _domain = "www.example.com"
    _uri = "/"
    _params = {}
    _body = {}
    _headers = {}
    
    def _constructParams(self):
        kwargs = {}
        
        kwargs['url'] = "{0}://{1}:{2}{3}".format(self._scheme, self._domain, self._port, self._uri)
        kwargs['method'] = self._method
        kwargs['params'] = self._params
        kwargs['data'] = json.dumps(self._body)
        kwargs['headers'] = self._headers
        
        return kwargs
    
    def __init__(self, env, di, args, **kwargs):
        super().__init__(env, di, args, **kwargs)
        
        if "uri" in kwargs:
            self._uri = kwargs["uri"]
        if "port" in kwargs:
            self._port = kwargs["port"]
        if "body" in kwargs:
            self._body = kwargs["body"]
        if "method" in kwargs:
            self._method = kwargs["method"]
        if "scheme" in kwargs:
            self._scheme = kwargs["scheme"]
        if "domain" in kwargs:
            self._domain = kwargs["domain"]
        if "params" in kwargs:
            self._params = kwargs["params"]
        if "headers" in kwargs:
            self._headers = kwargs["headers"]
    
    def run(self):
        return requests.request(**self._constructParams())
        
