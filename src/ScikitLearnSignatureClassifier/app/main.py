import logging
import os

import uvicorn
from fastapi import FastAPI, File, HTTPException

from app.model.signature_classifier import SignatureClassifier
from app.utils.file_utils import save_signature_file

app = FastAPI()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


@app.post("/classify",
          summary="Takes a png file and classifies it according the classifier",
          response_description="A JSON response in format {'is_signature': 0 (false) or 1 (true)}"
          )
async def classify(file_bytes: bytes = File()):

    signature_file: str
    try:
        signature_file = save_signature_file(file_bytes)
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))

    try:
        classifier = SignatureClassifier()
        is_signature = classifier.is_signature(signature_file)
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))

    return {'is_signature': int(is_signature)}


@app.post("/model/new",
          summary="Create new signature classifier model")
async def new_model(train_dataset_dir: str = os.path.join(os.curdir, 'signature_dataset')):
    try:
        classifier = SignatureClassifier()
        classifier.new_model(train_dataset_dir)
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))

    return "Classifier model was successfully created!"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)