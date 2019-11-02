from telegram.ext import BaseFilter

class _lidget(BaseFilter):
    def filter(self, message):
        return 'Lidget' in message.text

class _thorncliffe(BaseFilter):
    def filter(self, message):
        return 'Thorncliffe' in message.text

class _southgate(BaseFilter):
    def filter(self, message):
        return 'Southgate' in message.text

class _gym(BaseFilter):
    def filter(self, message):
        return 'Gym' in message.text

class _town(BaseFilter):
    def filter(self, message):
        return 'Town' in message.text