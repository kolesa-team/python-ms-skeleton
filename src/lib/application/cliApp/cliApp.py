from src.lib.application.baseApp import BaseApp


class CliApp(BaseApp):
    
    def getCommands(self):
        raise Exception("implement getCommands in {0}".format(self))
    
    def run(self):
        cmd = self._args.cmd
        commands = self.getCommands()
        
        if cmd not in commands: raise Exception("command not found")
        
        command = commands[cmd]['cmd'](self.getEnv(),self.getDi(),self.getArgs())
        
        command.run()
