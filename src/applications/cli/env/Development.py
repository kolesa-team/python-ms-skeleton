from src.applications.cli.env.Production import Production
from src.lib.application.env import Env


class Development(Env):
    
    def __init__(self):
        self.setParent(Production())
        self.setConfig(
            self.mergeConfig(
                self.getParent().getConfig(),
                {
                }
            ))
