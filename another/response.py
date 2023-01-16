
from .status import Status

class Response():
    data = None
    status = None
    
    def __init__(self, data = None, status = Status.HTTP_200_OK) -> None:
        self.data = data
        self.status = status
        
    def __str__(self) -> str:
        return f"Response: {self.data} {self.status}"
    
    def __repr__(self) -> str:
        return f"Response: {self.data} {self.status}"
    
    def __dict__(self) -> dict:
        return self.data,
        