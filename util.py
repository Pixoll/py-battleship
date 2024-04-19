import enum
from os import system, name
from random import randrange
from types import MappingProxyType
from typing import Any, NoReturn, Self


class Enum(enum.Enum):
    _member_map_: dict[str, Self]  # type: ignore
    _value2member_map_: dict[str, Self]  # type: ignore

    @classmethod
    def members(cls) -> MappingProxyType[str, Self]:
        return cls.__members__

    @classmethod
    def names(cls) -> list[str]:
        return cls._member_names_

    @classmethod
    def getRandom(cls) -> Self:
        names: list[str] = cls._member_names_
        index: int = randrange(len(names))
        return cls._member_map_[names[index]]  # type: ignore

    @classmethod
    def getByValue(cls, value: Any) -> Self | None:
        return cls._value2member_map_.get(value)  # type: ignore

    @classmethod
    def getByName(cls, name: str) -> Self | None:
        return cls.__members__.get(name)

    @classmethod
    def values(cls) -> list[Self]:
        return [x for x in cls.__members__.values()]


class IntEnum(enum.IntEnum, Enum):
    ""


class StrEnum(enum.StrEnum, Enum):
    ""


enumAuto = enum.auto


def clear() -> None:
    system("cls" if name == "nt" else "clear")


def pause() -> None:
    system("pause")


def close(code: str | int | None = None) -> NoReturn:
    print("\nClosing game...")
    pause()
    exit(code)


def toInt(str: str) -> int | None:
    try:
        return int(str)
    except ValueError:
        return None


def getInput(prompt: str) -> str:
    try:
        return input(prompt)
    except EOFError:
        close(0)
    except KeyboardInterrupt:
        close(0)


def center(text: str, length: int, filler: str = " ", includeRight: bool = True) -> str:
    rjustW: int = int((length + len(text)) / 2)
    result: str = text.rjust(rjustW, filler)
    if includeRight:
        result = result.ljust(length, filler)
    return result
