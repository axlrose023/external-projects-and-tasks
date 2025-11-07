from pydantic import BaseModel
from typing import List


class InitializeRequest(
    BaseModel
):
    csv_path: str


class ChatRequest(
    BaseModel
):
    user_id: str
    question: str


class MemoryRequest(
    BaseModel
):
    user_id: str
    memory_text: str


class InitializeResponse(
    BaseModel
):
    status: str
    count: int


class ChatResponse(
    BaseModel
):
    answer: str


class MemoryResponse(
    BaseModel
):
    status: str


class Cocktail(
    BaseModel
):
    id: int
    name: str
    alcoholic: str
    category: str
    glassType: str
    instructions: str
    ingredients: List[str]
    text: str
