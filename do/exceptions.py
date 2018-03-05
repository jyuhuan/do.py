class DoException(Exception):
    pass


class NoReturnException(DoException):
    def __init__(self):
        super(NoReturnException, self).__init__(
            'The do-routine does not return!')
