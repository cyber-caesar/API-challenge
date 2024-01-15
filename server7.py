from fastapi import Body, Depends, File, HTTPException, UploadFile, status, Security, FastAPI, Request
from fastapi.security import APIKeyHeader, APIKeyQuery
import requests
import json
from config import data_base

API_KEYS = [
    "9d207bf0-10f5-4d8f-a479-22ff5aeff8d1",
    "f47d4a2c-24cf-4745-937e-620a5963c0b8",
    "b7061546-75e8-444b-a2c4-f19655d07eb8",
]

data_list = requests.get(data_base).text
json_data = data_list.replace('\"', '"')
json_data = json.loads(json_data)

api_key_query = APIKeyQuery(name="api-key", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def get_api_key(
    request: Request,
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
) -> str:
    api_key = api_key_query or api_key_header
    request_method = request.method
    if request_method == "GET" and api_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key for GET method",
        )
    elif request_method == "POST" and api_key != API_KEYS[0]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key for POST method",
        )
    return api_key

app = FastAPI()

@app.get("/dog-list")
def get_data(api_key: str = Depends(get_api_key)):
    return json_data

@app.post("/match-json")
async def match_json(
    file: UploadFile = File(...),
    api_key: str = Depends(get_api_key),
):
    try:
        user_dog_content = await file.read()
        user_dog = json.loads(user_dog_content)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON file content.",
        )

    # Check if the provided JSON object matches any object in the list
    matched_item = next(
        (item for item in json_data if all(
            key in item and item[key] == user_dog[key]
            for key in user_dog
        )),
        None,
    )

    if matched_item:
        return "File Match successful: " + json.dumps(matched_item)
    else:
        raise HTTPException(
            status_code=404,
            detail="No match found for the provided JSON.",
        )
