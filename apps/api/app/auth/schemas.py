from pydantic import BaseModel, EmailStr, Field


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    name: str | None = Field(default=None, max_length=100)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class GoogleLoginIn(BaseModel):
    id_token: str  # Google ID token từ client (GIS)


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshIn(BaseModel):
    refresh_token: str


class UserOut(BaseModel):
    id: int
    email: str
    name: str | None = None
    role: str
    avatar_url: str | None = None


class EmailIn(BaseModel):
    email: EmailStr


class VerifyIn(EmailIn):
    code: str = Field(pattern=r"^\d{6}$")


class ResetIn(EmailIn):
    token: str = Field(min_length=20, max_length=200)
    password: str = Field(min_length=8, max_length=128)


class ProfileIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
