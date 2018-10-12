from src.lib.application.di import Di as BaseDi
import logging
from logging.handlers import SysLogHandler, WatchedFileHandler
from pygelf import GelfUdpHandler
from monolog import MonologHandler
import statsd


class Di(BaseDi):
    '''
    класс управления зависимостями
    '''
    _logger = None
    _statsd = None
    
    def init(self):
        'метод инициализирует сервисы'
        
        self.getLogger()
        self.getStatsD()
    
    def _getConfig(self):
        '''
        метод возвращает конфигурацию di
        
        :return: dict
        '''
        return self.getEnv().getConfig()['di']
    
    def getLogger(self):
        '''
        метод возвращает объект logger
        
        :return: logging.Logger
        '''
        if self._logger == None :
            
            config        = self._getConfig()['logger']
            udpConfig     = config['graylog']['UDP']
            sysLogConfig  = config['syslog']
            fileLogConfig = config['filelog']
            formater      = logging.Formatter(config['format'])
            
            logger = logging.getLogger()
            logger.setLevel(config['level'])
            
            if udpConfig['enable']:
                gelfHandler = GelfUdpHandler(
                    host = udpConfig['host'],
                    port = udpConfig['port']
                )
                
                gelfHandler.setFormatter(formater)
                logger.addHandler(gelfHandler)
            
            if fileLogConfig['enable']:
                fileHandler = WatchedFileHandler(
                    fileLogConfig['path'],
                    mode = 'a+'
                )
                
                fileHandler.setFormatter(formater)
                logger.addHandler(fileHandler)
            
            if sysLogConfig['enable']:
                monologHandler = MonologHandler(
                    SysLogHandler(
                        address = (sysLogConfig['host'], sysLogConfig['port'])
                    )
                )
                
                monologHandler.setFormatter(formater)
                logger.addHandler(monologHandler)
            
            self._logger = logger
            
        return self._logger
    
    def getStatsD(self):
        '''
        метод возвращает клиент для работы со statsd
        
        c.incr('foo')  # Increment the 'foo' counter.
        c.timing('stats.timed', 320)  # Record a 320ms 'stats.timed'.
        
        :return: statsd.client.udp.StatsClient
        '''
        
        if self._statsd == None:
            config = self._getConfig()['statsd']
            self._statsd = statsd.StatsClient(config['host'],config['port'],prefix = config['prefix'])
        
        return self._statsd
        