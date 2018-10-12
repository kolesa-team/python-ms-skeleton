from src.applications.cli.di import Di as cliDi
from src.applications.cli.env.Development import Development as cliDev
from src.applications.cli.env.Production import Production as cliProd
from src.applications.cli.app import CliApp
from src.applications.web.di import Di as webDi
from src.applications.web.env.Development import Development as webDev
from src.applications.web.env.Production import Production as webProd
from src.applications.web.app import WebApp
from src.lib.application.appRouter import *


class AppRouter(BaseAppRouter):
    
    def getApplications(self):
        return {
            "cli": {
                "app": CliApp,
                "env": {
                    "Development": cliDev,
                    "Production":  cliProd,
                },
                "di":  cliDi
            },
            "web": {
                "app": WebApp,
                "env": {
                    "Development": webDev,
                    "Production":  webProd,
                },
                "di":  webDi,
            },
        }
