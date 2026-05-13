class AuthBaseException(Exception):
    pass


class NoUsernameMatchError(AuthBaseException):
    def __init__(self, msg: str):
        self.message = msg
        super().__init__(self, self.message)