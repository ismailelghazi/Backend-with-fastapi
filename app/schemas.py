from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TranslationRequest(BaseModel):
    text: str
    direction: str  # "fr-en" or "en-fr"

class TranslationResponse(BaseModel):
    translation: str
