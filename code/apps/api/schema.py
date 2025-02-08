from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from ninja import Schema
from pydantic import BaseModel, Field, conint, constr, validator
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")


class Error(BaseModel):
    code: int
    message: str


class DataModel(BaseModel):
    result: Union[Dict[str, Any], List[Dict[str, Any]]]
    pagination: Optional[Dict[str, int]]


response_map = {200: DataModel, 404: Error, 403: Error}


class Filters(Schema):
    id: Optional[conint(gt=0)] = None
    page: conint(gt=0) = 1
    limit: conint(gt=0, le=100) = 8
