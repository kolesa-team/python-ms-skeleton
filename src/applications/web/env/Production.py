from src.applications.env.Production import Production as RootProduction
from src.applications.web.action.remarketingFeed import RemarketingFeedAction
from src.applications.web.action.modelExample import ModelExampleAction


class Production(RootProduction):
    
    def __init__(self):
        self.setParent(RootProduction())
        self.setConfig(
            self.mergeConfig(
                self.getParent().getConfig(),
                {
                    "web-app": {
                        "host":   "0.0.0.0",
                        "port":   8899,
                        "routes": {
                            "marketfeed": {
                                "url":    "/marketfeed/",
                                "action": RemarketingFeedAction,
                                "kwargs": {}
                            },
                            "modelexample" : {
                                'url' : "/modelExample/",
                                "action" : ModelExampleAction,
                                "kwargs" : {}
                            }
                        },
                    }
                }
            ))
