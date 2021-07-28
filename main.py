from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from starlette.responses import JSONResponse
from starlette.requests import Request

import json
import pymongo
import urllib


app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.route("/", methods=["GET", "POST"])
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/fruits")
async def fruits(request: Request):
    body = await request.json()
    access_key_id = urllib.parse.quote_plus(body['AccessKeyId'])
    secret_key_id = urllib.parse.quote_plus(body['SecretAccessKey'])
    session_token = urllib.parse.quote_plus(body['SessionToken'])
    # uri = f"mongodb://{access_key_id}:" \
    #       f"{secret_key_id}@cluster0.bjrye.mongodb.net/?authMechanism=MONGODB-AWS&authSource=%24external" \
    #       f"&authMechanismProperties=AWS_SESSION_TOKEN:{session_token}"
    uri = f"mongodb+srv://{access_key_id}:{secret_key_id}@cluster0.bjrye.mongodb.net/myFirstDatabase" \
          f"?authSource=%24external&authMechanism=MONGODB-AWS&retryWrites=true&w=majority" \
          f"&authMechanismProperties=AWS_SESSION_TOKEN:{session_token}"
    mongo_client = pymongo.MongoClient(uri)
    mongo_db = mongo_client.test
    fruit_list = []
    fruits = mongo_db['marketplace'].find({}, {'_id': 0, 'name': 1, 'price': 1, 'quantity': 1})
    for fruit in fruits:
        fruit_list.append(fruit)
    print(fruit_list)
    return JSONResponse({"fruits": json.dumps(fruit_list)})


