class ProjectServiceException(Exception):
    def __init__(self, message: str, error_code: int):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
        
    def __str__(self):
        return f'{self.message} (Error code: {self.error_code})'
        

class ProjectNotFoundException(ProjectServiceException):
    def __init__(self):
        super().__init__('Project not found', 404)
        

class ProjectAccessIsNotAllowedException(ProjectServiceException):
    def __init__(self):
        super().__init__('Access is not allowed', 403)
            