import pandas as pd
from io import StringIO

import uvicorn
from fastapi import FastAPI, File, HTTPException

app = FastAPI()

@app.post("/classify", 
          summary="Takes a document docx file and classifies it according the classifier",
          response_description="A JSON response in format {'document_name':name, 'text': text, 'class_id': ID}"
         )
async def classify(textDocument: HttpTextDocument):
    return {'document_name': textDocument.name, 'text': textDocument.text, 'class_id': 'TEST'}

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


@app.post("/model/new",
          summary="Create new classifier model",
          response_description="Information string about successfully classifier model created")
async def new_model(file_bytes: bytes = File(),
                    code_page: str = 'windows-1251',
                    delimiter: str = ';',
                    x_field_name: str = 'shortcontent',
                    y_field_name: str = 'actkind'):

    try:
        data = pd.read_csv(StringIO(file_bytes.decode(code_page)), delimiter=delimiter)
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))

    classifier = Classifier()
    classifier.new_model(train=data, x_field_name=x_field_name, y_field_name=y_field_name)

    return "Classifier model was successfully created!"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
