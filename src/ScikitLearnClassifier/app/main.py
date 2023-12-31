import pandas as pd
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
        category = classifier.classified_text(text_document.text)
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))

    return {'text_category': int(category)}


@app.post("/model/new",
          summary="Create new classifier model",
          response_description="Information string about successfully classifier model created")
async def new_model(x_field_name: str,
                    y_field_name: str,
                    file_bytes: bytes = File(),
                    code_page: str = 'windows-1251',
                    delimiter: str = ';'):

    try:
        data = pd.read_csv(StringIO(file_bytes.decode(code_page)), delimiter=delimiter, on_bad_lines='skip')
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))

    classifier = Classifier()
    classifier.new_model(train=data, x_field_name=x_field_name, y_field_name=y_field_name)

    return "Classifier model was successfully created!"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
