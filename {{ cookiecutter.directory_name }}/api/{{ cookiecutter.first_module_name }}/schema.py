from datetime import datetime
from typing import Literal, Optional
from pydantic import validator

from pydantic import BaseModel
import pytz



class {{cookiecutter.first_model_name}}CreateRequestBody(BaseModel):
    pass