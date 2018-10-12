import logging, os.path

from src.lib.application.env import Env
from logging.handlers import SYSLOG_UDP_PORT

# TODO вынести текущие конфиги в development окружение а эти заменить на

class Production(Env):
    
    def __init__(self):
        self.setParent(Env())
        self.setConfig(
            self.mergeConfig(
                self.getParent().getConfig(),
                {
                    "di":      {
                        'statsd': {
                            'host':   'graphite1.alahd.kz.dev.bash.kz', # TODO заменить на production конфиг
                            'port':   8125,
                            'prefix': 'ms-py-example', # example заменить на конкретный микросервис
                        },
                        'logger': {
                            'format':  '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            'level':   logging.DEBUG,  # TODO поменять на прод настройки
                            'filelog': {
                                'enable': True,
                                'path':   'src/log/info.log',
                            },
                            'syslog':  {
                                'enable': False,
                                'host':   '127.0.0.1',
                                'port':   SYSLOG_UDP_PORT,
                            },
                            'graylog': {
                                'UDP': {
                                    'enable': True,
                                    'host':   'graylog1.alahd.kz.dev',  # udp host TODO поменять на прод настройки
                                    'port':   12203,  # TODO поменять на прод настройки
                                }
                            }
                        },
                    },
                    "cli-app": {
                    
                    },
                    "web-app": {
                    }
                }
            ))
