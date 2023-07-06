import logging
from typing import Any

from fastapi.routing import APIRouter
from sqlalchemy import select

from db.session import SessionLocal

from .models import {{cookiecutter.first_model_name}}
from .schema import {{cookiecutter.first_model_name}}CreateRequestBody

router = APIRouter()


@router.get("/{{cookiecutter.first_model_name|lower}}/latest")
async def get_{{cookiecutter.first_model_name|lower}}() -> Any:

    query = select({{cookiecutter.first_model_name}})
    async with SessionLocal() as session:
        resp = await session.execute(query)
    return resp.all()


@router.post("/{{cookiecutter.first_model_name|lower}}")
async def post_{{cookiecutter.first_model_name|lower}}(body: {{cookiecutter.first_model_name}}CreateRequestBody) -> Any:
    async with SessionLocal() as session:
        sched = {{cookiecutter.first_model_name}}(**body.dict())
        try:
            session.add(sched)
        except Exception:
            await session.rollback()
            await session.commit
            await session.commit