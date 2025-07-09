from pydantic import BaseModel

class SuccessResponse(BaseModel):
    message: str
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Operation completed successfully"
            }
        }

class ErrorResponse(BaseModel):
    detail: str
    
    class Config:
        schema_extra = {
            "example": {
                "detail": "Error message"
            }
        }