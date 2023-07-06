import uvicorn
from fastapi.applications import FastAPI

from bootstrap import BootstrapApp
from config import settings

fapi = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API.V1_STR}/openapi.json")

bootstrap = BootstrapApp(fapi, settings)

bootstrap.create_app()
app = bootstrap.app


if __name__ == "__main__":
    uvicorn.run(app, host=settings.API.INTERFACE, port=settings.API.PORT)
