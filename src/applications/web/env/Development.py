from src.applications.web.env.Production import Production
from src.lib.application.env import Env


class Development(Env):
    
    def __init__(self):
        self.setParent(Production())
        self.setConfig(
            self.mergeConfig(
                self.getParent().getConfig(),
                {
                    "web-app": {
                        "routes": {
                            "marketfeed": {
                                "kwargs": {
                                    "test3": "test3",
                                    "test4": "test4",
                                }
                            }
                        },
                    }
                }
            ))
