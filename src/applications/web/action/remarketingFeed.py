from src.lib.application.webApp.action import Action


class RemarketingFeedAction(Action):
    def get(self):
        self.write("RemarketingFeedAction")
