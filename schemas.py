from typing import List
from pydantic import BaseModel


class UploadVideo(BaseModel):
    title: str
    description: str


class User(BaseModel):
    id: int 
    username: str 


class GetListVideo(BaseModel):
    id: int
    title: str
    description: str


class GetVideo(GetListVideo):
    user: User
