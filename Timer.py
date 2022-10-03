import datetime

class Timer:
    def __init__(self):
        self.s = datetime.datetime.now()
    def start(self):
        self.s = datetime.datetime.now()
    def get(self):
        end = datetime.datetime.now()
        return str(end - self.s)[:-4]

timer = Timer()