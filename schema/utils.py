import re
from enum import StrEnum
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Literal, Type, Union

from pydantic import (
    BaseModel,
    ConstrainedStr,
    Field,
    conint,
    conlist,
    constr,
    create_model,
)
from typing_extensions import LiteralString

if TYPE_CHECKING:
    ID = str
    JStr = str
    JList = list
    JPositive = int
else:
    ID = constr(regex=r"^[a-zA-Z0-9_]+$")
    JStr = constr(min_length=1)
    JList = conlist(min_items=1, item_type=JStr)
    JPositive = conint(gt=0)


def to_classname(text: str) -> str:
    return "".join(t.capitalize() for t in text.split("_"))


def fold_text(text: str) -> str:
    "replace all whitespaces into single space"
    return re.sub(r"\s+", " ", text)  # type: ignore


def get_desc(text: str, fold=True):
    return (fold_text if fold else dedent)(text.lstrip())


def field(*args: Any, fold=True, **kwargs: Any):
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


def reqfield(desc: str, fold=True, **kwargs: Any):
    return field(..., desc, fold=fold, **kwargs, required=True)


def enum_model(
    name: str, *args: str, fold=True, **kwargs: Any
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


_ID = r"[a-zA-Z0-9_]+"


class RegexType(StrEnum):
    LITERAL = r"^{value}$"
    PREFIX = rf"^{{value}}_{_ID}"
    SUFFIX = rf"^{_ID}_{{value}}$"

    @classmethod
    def as_str(cls, regex: "RegexType", plural=False) -> str:
        def pluralize(text: str, on_plural: str) -> str:
            return text if not plural else f"{text}{on_plural}"

        match regex:
            case cls.LITERAL:
                return pluralize("id", "s")
            case cls.PREFIX:
                return pluralize("prefix", "es")
            case cls.SUFFIX:
                return pluralize("suffix", "es")


def one_of(texts: tuple[LiteralString, ...], regex: RegexType) -> str:
    values = ", ".join(f"`{s}`" for s in texts)

    return f"The special {regex.as_str(regex, len(texts) > 1)} {values}"


def id_with(name: str, regex: re.Pattern[str]) -> Type["Model"]:  # type: ignore
    """creates a constrained regex string"""
    return create_model(
        to_classname(name),
        regex=regex,
        __base__=ConstrainedStr,  # type: ignore
    )


def id_from(
    name: str,
    template: str,
    names: tuple[LiteralString, ...],
    regex: RegexType = RegexType.LITERAL,
    **kwargs: Any,
):
    desc = template.format(id=one_of(names, regex))
    ids = [id_with(name, re.compile(regex.format(value=it))) for it in names]
    IDsType = Union[*ids]  # type: ignore

    return create_model(
        to_classname(name),
        __root__=(IDsType, field(desc, **kwargs)),
        __base__=BaseModel,
    )


def object_or_list(name: str, model: Type["BaseModel"]):
    return create_model(
        to_classname(name),
        __root__=(model | list[model], ...),  # type: ignore
        __base__=BaseModel,
    )
