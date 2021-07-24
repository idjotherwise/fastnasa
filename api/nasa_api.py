import fastapi
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from models.validation_error import ValidationError
from services import nasa_service

templates = Jinja2Templates('templates')
router = fastapi.APIRouter()

@router.get('/api/pod', response_class=HTMLResponse)
async def pod(request: Request):
    try:
        data = await nasa_service.get_report_async()
        return templates.TemplateResponse('home/pod.html', {'request': request, 'data': data})
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)
    except Exception as x:
        print(f"Server crashed while processing request: {x}")
        return fastapi.Response(content='Error processing your request.', status_code=500)