import uvicorn
from fastapi import FastAPI, HTTPException

from entities.request_entities import HttpTextDocument
from app.model.classifier import Classifier

app = FastAPI()


@app.post("/classify",
          summary="Takes a string and classifies it according the classifier",
          response_description="A JSON response in format {'text_category': category}"
          )
async def classify(text_document: HttpTextDocument):
    try:
        classifier = Classifier()
        category = classifier.classified_text(text_document.text)
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))

    return {'text_category': category}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
