from src.applications.env.Production import Production as RootProduction


class Production(RootProduction):
    
    def __init__(self):
        self.setParent(RootProduction())
        self.setConfig(
            self.mergeConfig(
                self.getParent().getConfig(),
                {
                }
            ))
