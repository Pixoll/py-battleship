from io import TextIOWrapper
from typing import Any, Literal, TypeAlias

OpenTextMode: TypeAlias = Literal[
    'r+', '+r', 'rt+', 'r+t', '+rt', 'tr+', 't+r', '+tr', 'w+', '+w', 'wt+', 'w+t', '+wt', 'tw+',
    't+w', '+tw', 'a+', '+a', 'at+', 'a+t', '+at', 'ta+', 't+a', '+ta', 'x+', '+x', 'xt+', 'x+t',
    '+xt', 'tx+', 't+x', '+tx', 'w', 'wt', 'tw', 'a', 'at', 'ta', 'x', 'xt', 'tx', 'r', 'rt', 'tr',
    'U', 'rU', 'Ur', 'rtU', 'rUt', 'Urt', 'trU', 'tUr', 'Utr'
]

class Settings:
    CONFIG_FILE = "./battleship.properties"

    @staticmethod
    def getConfigFile(mode: OpenTextMode = "r") -> TextIOWrapper:
        try:
            return open(Settings.CONFIG_FILE, mode, encoding = "utf-8")
        except:
            tempFile = open(Settings.CONFIG_FILE, "w")
            tempFile.close()
            return open(Settings.CONFIG_FILE, mode, encoding = "utf-8")

    def __init__(self, defaults: dict[str, Any]) -> None:
        self.values: dict[str, str] = {}

        configFile: TextIOWrapper = Settings.getConfigFile()
        rawData: list[str] = configFile.readlines()
        configFile.close()

        for line in rawData:
            if not len(line.strip()) or line.startswith("#"):
                continue
            [key, value] = line.split("=", 1)
            self.values[key] = value.replace("\n", "").replace("''", "'")

        for k, v in defaults.items():
            if self.values.get(k):
                continue
            self.setValue(k, v)

    def setValue(self, key: str, value: Any) -> None:
        if self.values.get(key) and self.values[key] == value:
            return

        self.values[key] = str(value)
        lines: list[str] = [f"{k}={v}\n" for k, v in self.values.items()]
        configFile: TextIOWrapper = Settings.getConfigFile("w")
        configFile.writelines(lines)
        configFile.close()

    def setValues(self, settings: dict[str, Any]) -> None:
        for k, v in settings.items():
            self.setValue(k, v)

    def getValue(self, key: str) -> str:
        return self.values.get(key, "")

settings = Settings({
    "lang": "en",
    "langFolder": "./lang/",
    "savesFolder": "./saves/",
    "firstLaunch": True
})
