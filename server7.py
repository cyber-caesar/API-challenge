from fastapi import Body, Depends, File, HTTPException, UploadFile, requests, status, Security, FastAPI
from fastapi.security import APIKeyHeader, APIKeyQuery
from pydantic import BaseModel
import json

API_KEYS = [
    "9d207bf0-10f5-4d8f-a479-22ff5aeff8d1",
    "f47d4a2c-24cf-4745-937e-620a5963c0b8",
    "b7061546-75e8-444b-a2c4-f19655d07eb8",
]

data_list = [
    {
        "name": "Labrador Retriever",
        "lifespan": "10-12 years",
        "size": "Large",
        "temperament": "Outgoing, Even Tempered, Gentle",
        "origin": "Canada",
    },
    {
        "name": "German Shepherd",
        "lifespan": "9-13 years",
        "size": "Large",
        "temperament": "Loyal, Confident, Courageous",
        "origin": "Germany",
    },
    {
        "name": "Golden Retriever",
        "lifespan": "10-12 years",
        "size": "Large",
        "temperament": "Intelligent, Friendly, Devoted",
        "origin": "United Kingdom",
    },
    {
        "name": "French Bulldog",
        "lifespan": "10-12 years",
        "size": "Small",
        "temperament": "Adaptable, Playful, Smart",
        "origin": "France",
    },
]

api_key_query = APIKeyQuery(name="api-key", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
) -> str:
    if api_key_query in API_KEYS:
        return api_key_query
    if api_key_header in API_KEYS:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )

app = FastAPI()

@app.get("/dog-list")
def get_data(api_key: str = Depends(get_api_key)):
    
    return data_list

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
    matched_item = next((item for item in data_list if all(item[key] == user_dog[key] for key in item)), None)

    
    if matched_item:
        return matched_item
    else:
        raise HTTPException(
            status_code=404,
            detail="No match found for the provided JSON.",
        )