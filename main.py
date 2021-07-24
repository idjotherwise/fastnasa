import json
from pathlib import Path

import uvicorn
from starlette.staticfiles import StaticFiles

from api import nasa_api
from fastapi import FastAPI

from services import nasa_service

api = FastAPI()


def configure_routing():
    api.mount('/static', StaticFiles(directory='static'), name='static')
    api.include_router(nasa_api.router)


def configure():
    configure_routing()
    configure_api_keys()

def configure_api_keys():
    file = Path('settings.json').absolute()
    if not file.exists():
        print(f"WARNING: {file} file not found, you cannot continue. Please see settings_template.json")
        raise Exception("settings.json file not found, you cannot continue please see settings_template.json")
    with open("settings.json") as fin:
        settings = json.load(fin)
        nasa_service.api_key = settings.get("api_key")

if __name__ == '__main__':
    configure()
    uvicorn.run('main:api', reload=True)
else:
    configure()