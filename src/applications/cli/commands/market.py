# -*- coding: utf-8 -*-
import json

from src.lib.application.cliApp.command import Command
from src.lib.application.httpClient import HttpClient


class MarketFeed(Command):
    
    def run(self):
        pass


class SiteMapParser(Command):
    def run(self):
        params = {
            "scheme":  "http",
            "domain":  "api.kolesa.fd.dev",
            "uri":     "/v1/adverts/getOne.json",
            "params":  {
                "storageId":  "live",
                "id":  "8707295",
                "appId":  "438530889024",
                "appKey": "31c2954f58c2e18a310d8acab7e99fa1"
            },
            "method":  "GET",
        }
        
        cmd = (HttpClient(self.getEnv(), self.getDi(), self.getArgs(), **params))
        
        result = cmd.run()
        
        print(json.loads(result.text.encode("utf-8")))
