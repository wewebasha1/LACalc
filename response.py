class Response:
    def __init__(self, message, matrix):
        self.message = message
        self.matrix = matrix

    def get_message(self):
        return self.message

    def get_matrix(self):
        return self.matrix
