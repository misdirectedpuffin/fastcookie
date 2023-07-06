# Import all the models, so that Base has them before being
# imported by Alembic
from api.{{cookiecutter.first_module_name}}.models import *  # noqa
