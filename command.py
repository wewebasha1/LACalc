class Command:
    def __init__(self, action, parameters):
        self.action = action
        self.parameters = parameters

    def get_action(self):
        return self.action

    def get_parameter(self):
        return self.parameters
