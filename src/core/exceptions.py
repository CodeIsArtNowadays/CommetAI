from fastapi import status

class CustomException(Exception):
    def __init__(self, message: str, error_code: int):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ProjectServiceException(CustomException):
    pass
        

class ProjectNotFoundException(ProjectServiceException):
    def __init__(self):
        super().__init__('Project not found', status.HTTP_304_NOT_MODIFIED)
        

class ProjectAccessIsNotAllowedException(ProjectServiceException):
    def __init__(self):
        super().__init__('Access is not allowed', status.HTTP_403_FORBIDDEN)


class GithubApiException(CustomException):
    def __init__(self, status_code):
        super().__init__('Github bad response', status_code)
        

class GithubUnAutharize(CustomException):
    def __init__(self):
        super().__init__('Github bad autharization', status.HTTP_401_UNAUTHORIZED)
        
class WebhookNotVerify(CustomException):
    def __init__(self):
        super().__init__('Webhook not verify', status.HTTP_401_UNAUTHORIZED)
        

class LLMException(CustomException):
    def __init__(self):
        super().__init__('LLM error', status.HTTP_500_INTERNAL_SERVER_ERROR)