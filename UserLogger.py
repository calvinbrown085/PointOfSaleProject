class Logger:
    def __init__(self):
        self.x = []

    def logUser(self, user, endpoint, time):
        self.x.append((user,endpoint,time))

    def resetLogs(self):
        self.x = []

    def getUserLog(self):
        return self.x
