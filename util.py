import os
from typing import NoReturn

def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def pause() -> None:
    os.system("pause")

def close(code: str | int | None = None) -> NoReturn:
    print("Closing game...")
    pause()
    exit(code)

def toInt(str: str) -> int | None:
    try:
        return int(str)
    except:
        return None

def getInput(prompt: str) -> str:
    try:
        return input(prompt)
    except:
        close(0)

def center(text: str, length: int, filler: str = " ", includeRight: bool = True) -> str:
    rjustW: int = int((length + len(text)) / 2)
    result: str = text.rjust(rjustW, filler)
    if includeRight:
        result = result.ljust(length, filler)
    return result
