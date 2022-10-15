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


def field(*args: str, fold: bool = True, **kwargs: Any):
    """one args: description, two args: default, description"""

    match len(args):
        case 1:
            default, description = ..., args[0]
        case 2:
            default, description = args  # type: ignore

        case _:
            raise ValueError(
                f"field() takes 1 or 2 positional arguments, but got {args}"
            )

    desc = (fold_text if fold else dedent)(description)  # type: ignore
    return Field(
        default,
        description=desc,
        markdownDescription=desc,
        **kwargs,
    )


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
