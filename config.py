from io import TextIOWrapper
from typing import Any, Literal, TypeAlias

OpenTextMode: TypeAlias = Literal[
    'r+', '+r', 'rt+', 'r+t', '+rt', 'tr+', 't+r', '+tr', 'w+', '+w', 'wt+', 'w+t', '+wt', 'tw+',
    't+w', '+tw', 'a+', '+a', 'at+', 'a+t', '+at', 'ta+', 't+a', '+ta', 'x+', '+x', 'xt+', 'x+t',
    '+xt', 'tx+', 't+x', '+tx', 'w', 'wt', 'tw', 'a', 'at', 'ta', 'x', 'xt', 'tx', 'r', 'rt', 'tr',
    'U', 'rU', 'Ur', 'rtU', 'rUt', 'Urt', 'trU', 'tUr', 'Utr'
]

class Config:
    CONFIG_FILE = "./battleship.properties"

    @staticmethod
    def getConfigFile(mode: OpenTextMode = "r") -> TextIOWrapper:
        try:
            return open(Config.CONFIG_FILE, mode, encoding = "utf-8")
        except:
            tempFile = open(Config.CONFIG_FILE, "w")
            tempFile.close()
            return open(Config.CONFIG_FILE, mode, encoding = "utf-8")

    def __init__(self, defaults: dict[str, Any]) -> None:
        self.settings: dict[str, str] = {}

        configFile: TextIOWrapper = Config.getConfigFile()
        rawData: list[str] = configFile.readlines()
        configFile.close()

        for line in rawData:
            if not len(line.strip()) or line.startswith("#"):
                continue
            [key, value] = line.split("=", 1)
            self.settings[key] = value.replace("\n", "").replace("''", "'")

        for k, v in defaults.items():
            if self.settings.get(k):
                continue
            self.setSetting(k, v)

    def setSetting(self, key: str, value: Any) -> None:
        if self.settings.get(key) and self.settings[key] == value:
            return

        self.settings[key] = str(value)
        lines: list[str] = [f"{k}={v}\n" for k, v in self.settings.items()]
        configFile: TextIOWrapper = Config.getConfigFile("w")
        configFile.writelines(lines)
        configFile.close()

    def setSettings(self, settings: dict[str, Any]) -> None:
        for k, v in settings.items():
            self.setSetting(k, v)

    def getSetting(self, key: str) -> str:
        return self.settings.get(key, "")

config = Config({
    "lang": "en",
    "langFolder": "./lang/",
    "savesFolder": "./saves/",
    "firstLaunch": True
})
