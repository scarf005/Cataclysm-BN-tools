import re
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Literal, Type, Union

from pydantic import BaseModel, Field, conlist, constr, create_model

if TYPE_CHECKING:
    ID = str
    JStr = str
    JList = list
else:
    ID = constr(regex=r"^[a-zA-Z0-9_]+$")
    JStr = constr(min_length=1)
    JList = conlist(min_items=1, item_type=JStr)


def to_classname(text: str) -> str:
    return "".join(t.capitalize() for t in text.split("_"))


def fold_text(text: str) -> str:
    "replace all whitespaces into single space"
    return re.sub(r"\s+", " ", text)  # type: ignore


def get_desc(text: str, fold: bool = True):
    return (fold_text if fold else dedent)(text)


def field(*args: Any, fold: bool = True, **kwargs: Any):
    """one args: description, two args: default, description"""

    desc = get_desc(args[-1], fold=fold)

    args_dict: dict[str, Any] = {
        "description": desc,
        "markdownDescription": desc,
    }

    match args:
        case [str()]:
            ...
        case [_ as default, str()]:
            args_dict["default"] = default
        case _:
            raise ValueError(
                f"field() takes 1 or 2 positional arguments, but got {args}"
            )

    return Field(**(args_dict | kwargs))


def reqfield(desc: str, fold: bool = True, **kwargs: Any):
    return field(..., desc, fold=fold, **kwargs, required=True)


def enum_model(
    name: str, *args: str, fold: bool = True, **kwargs: Any
) -> Type[BaseModel]:
    """one args: description, two args: default, description"""

    return create_model(
        to_classname(name),
        __root__=(Literal[name], field(*args, fold=fold, **kwargs)),  # type: ignore
        __base__=BaseModel,
    )


def enums_from(data: dict[str, str]) -> Any:
    categories_classes = (enum_model(k, v) for k, v in data.items())
    return Union[*categories_classes]  # type: ignore
