from typing import Dict, Any, Type

import attr
from box import Box
from pydantic import BaseModel
from returns.curry import curry


def boxify(data: Dict[str, Any]) -> Box:
    return Box(
        data,
        frozen_box=True,
        default_box=True,
        default_box_create_on_get=False,
        default_box_none_transform=False,
        box_dots=True,
    )


def to_record(data: Dict[str, Any]) -> Box:
    return boxify(
        {
            "id": None,
            **dict(data),
        }
    )


@curry
def dto_from_attr(ctor: Type, data: Any) -> Type:
    return ctor(**attr.asdict(data))


def boxify_params(model: BaseModel) -> Box:
    return boxify(model.dict(exclude_unset=True))
