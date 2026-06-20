from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import string
import json
from fastapi.responses import RedirectResponse

app = FastAPI()

try:
    with open("urls.json", "r") as f:
        url_mapping = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    url_mapping = {}

class URLRequest(BaseModel):
    url: str

@app.post("/shorten")
def shorten_url(request: URLRequest):
    longURL = request.url

    while True:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if code not in url_mapping:
            break

    if longURL in url_mapping:
        url_mapping[longURL]= code
    else:
        url_mapping[longURL] = code

    with open("urls.json", "w") as f:
        json.dump(url_mapping, f, indent=2)

    print(url_mapping)
    return {"short_code": code}


@app.get("/{code}")
def redirect_to_url(code: str):
    if code not in url_mapping:
        raise HTTPException(status_code=404, detail="Short code not found")
    return RedirectResponse(url=url_mapping[code])