import argparse, os


class BaseAppRouter(object):
    '''
    класс собирает и запускает нужное приложение
    с окружением и зависимостями
    '''
    
    _applicationName = None
    "cli arg --app"
    
    _environmentName = None
    "cli arg --env"
    
    _applications = None
    " результат метода self.getApplications()"
    
    _application = None
    "собранный аппликейшн src.lib.application.baseApp.BaseApp"
    
    _environment = None
    "собранный объект окружения src.lib.application.env.Env"
    
    _command = None
    "cli arg --cmd"
    
    def __init__(self):
        pass
    
    def _setCliArgs(self, args):
        '''
        устанавливает переданные cli аргументы

        :param args: объект аргументов
        :return:
        '''
        if 'app' in args and 'env' in args:
            self._applicationName = getattr(args, 'app')
            self._environmentName = getattr(args, 'env')
            
            if 'cmd' in args:
                self._command = getattr(args, 'cmd')
        
        else:
            raise Exception("you must provide application and environment name ")
    
    def _getDi(self, env, args):
        '''
        собирает и возвращает объект зависимостей

        :param env: объект окружения
        :param args: cli аргументы
        :return:
        '''
        di = self._applications[self._applicationName]['di'](env, args)
        di.init()
        
        return di
    
    def _getEnv(self):
        '''
        собирает и возвращает объект окружения

        :return: object
        '''
        if self._environmentName not in self._applications[self._applicationName]['env']:
            raise Exception("Provide correct environment name")
        env = self._applications[self._applicationName]['env'][self._environmentName]()
        env.BASE_PATH = os.getenv('BASE_PATH', None)
        
        if env.BASE_PATH == None:
            raise Exception('define BASE_PATH environment variable - project root directory')
        return env
    
    def getApplications(self):
        raise Exception("implement getApplications method")
    
    def getNamedArgs(self):
        return {
            "--app": "app name to start",
            "--env": "app inveronment",
            "--cmd": "cli command"
        }
    
    def resolve(self):
        '''
        метод собирает приложение с заданным окружением и собранными зависимостями
        
        :return: src.lib.application.appRouter.BaseAppRouter
        '''
        args = self.getNamedArgs()
        parser = argparse.ArgumentParser()
        
        for k in args:
            parser.add_argument(k, help = args[k])
        
        self._applications = self.getApplications()
        
        args = parser.parse_args()
        
        self._setCliArgs(args)
        
        # конфигурируем приложение
        if (self._applicationName in self._applications):
            env = self._getEnv()
            di = self._getDi(env, args)
            self._application = self._applications[self._applicationName]['app'](env, di, args)
        
        else:
            raise Exception('Provide correct application name')
        
        return self
    
    def run(self):
        '''
        метод запускает приложение
        '''
        self._application.run()
