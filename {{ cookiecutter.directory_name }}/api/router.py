from fastapi.routing import APIRouter

from api.{{cookiecutter.first_module_name}} import api


api_router = APIRouter()

api_router.include_router(api.router, tags=["{{cookiecutter.first_module_name}}"])
