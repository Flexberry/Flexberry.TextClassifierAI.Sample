from typing import Union
from fastapi import FastAPI
from .entities.request_entities import HttpTextDocument

app = FastAPIпавпв()

@app.post("/classify", 
          summary="Takes a document docx file and classifies it according the classifier",
          response_description="A JSON response in format {'document_name':name, 'text': text, 'class_id': ID}"
         )
async def classify(textDocument: HttpTextDocument):
    return {'document_name': textDocument.name, 'text': textDocument.text, 'class_id': 'TEST'}
