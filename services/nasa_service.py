from typing import Optional

import httpx
from httpx import Response
from models.validation_error import ValidationError

api_key: Optional[str] = None


async def get_report_async() -> dict:
    url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'
    async with httpx.AsyncClient() as client:
        resp: Response = await client.get(url)
        if resp.status_code != 200:
            raise ValidationError(resp.text, status_code=resp.status_code)

    data = resp.json()

    # check that the media type is an image
    assert data['media_type'] == 'image'

    pod = {
            'title': data['title'],
            'image_url': data['url'],
            'explanation': data['explanation'],
            'date': data['date']
           }

    return pod