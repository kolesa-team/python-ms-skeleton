# -*- coding: utf-8 -*-
from src.applications.appRouter import AppRouter
import os

if __name__ == '__main__':
    os.environ['BASE_PATH'] = os.path.basename(os.path.realpath(__file__))
    
    appRouter = AppRouter()
    appRouter.resolve().run()
