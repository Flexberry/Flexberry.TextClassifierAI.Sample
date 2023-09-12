from pydantic import BaseModel


class HttpTextDocument(BaseModel):
    name: str
    text: str
