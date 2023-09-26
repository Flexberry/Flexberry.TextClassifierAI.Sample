from io import StringIO

import uvicorn
from fastapi import FastAPI, File, HTTPException

from app.entities.request_entities import HttpTextDocument
from app.model.classifier import Classifier

app = FastAPI()


@app.post("/classify",
          summary="Takes a string and classifies it according the classifier",
          response_description="A JSON response in format {'text_category': category}"
          )
async def classify(text_document: HttpTextDocument):
    try:
        classifier = Classifier()
        category = classifier.classify_text(text_document.text)
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))

    return {'text_category': category}


@app.post("/train",
          summary="Create new classifier model",
          response_description="Information string about successfully classifier model created")
async def train(x_field_name: str,
                y_field_name: str,
                file_bytes: bytes = File(),
                code_page: str = 'windows-1251',
                delimiter: str = ';'):
    try:
        data = StringIO(file_bytes.decode(code_page))
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))

    try:
        classifier = Classifier()
        classifier.train_model(csv=data, text_column=x_field_name, label_column_name=y_field_name, delimiter=delimiter)
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))

    return "Classifier model was successfully created!"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
