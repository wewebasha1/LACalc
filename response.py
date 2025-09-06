class Response:
    def __init__(self, message, matrix):
        self.message = message
        self.matrix = matrix
        self.undo_command = None

    def get_message(self):
        return self.message

    def get_matrix(self):
        return self.matrix

    def get_undo_command(self):
        return self.undo_command

    def set_undo_command(self, command):
        self.undo_command = command
