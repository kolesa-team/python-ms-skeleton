from src.lib.application.cliApp.cliApp import CliApp as BaseCliApp
from src.applications.cli.commands.market import *

class CliApp(BaseCliApp):
    def getCommands(self):
        return {
            "marketfeed" : {
                "cmd": MarketFeed
            },
            "sitemap-parser" : {
                "cmd" : SiteMapParser
            }
        }
    
    pass
