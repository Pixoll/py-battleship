from config import config
from os import listdir
from typing import Any

class Lang:
    LANG_FOLDER = config.getSetting("langFolder")

    def __init__(self) -> None:
        self.lang = config.getSetting("lang")
        self.langs: dict[str, dict[str, str]] = {}

        for file in listdir(Lang.LANG_FOLDER):
            lang: str = file.split(".")[0]
            langMessages: dict[str, str] = {}

            langFile = open(Lang.LANG_FOLDER + file, encoding = "utf-8")
            for line in langFile:
                if not len(line.strip()) or line.startswith("#"):
                    continue
                [key, value] = line.split("=", 1)
                langMessages[key] = value.replace("\n", "").replace("''", "'")

            langFile.close()
            self.langs[lang] = langMessages

    def setLang(self, lang: str) -> None:
        self.lang = lang
        config.setSetting("lang", lang)

    def getLangs(self) -> list[str]:
        return [l for l in self.langs.keys()]

    def getLangNames(self) -> list[str]:
        return [l["langName"] for l in self.langs.values()]

    def getLangName(self, id: str) -> str:
        return self.langs[id]["langName"]

    def getLangId(self, name: str) -> str:
        for k, v in self.langs.items():
            if v["langName"] == name:
                return k
        return "en"

    def getMessage(self, key: str, *args: Any) -> str:
        value: str = self.langs[self.lang][key]
        if not len(args):
            return value
        for i in range(len(args)):
            value = value.replace(f"{{{i}}}", str(args[i]))
        return value

lang = Lang()
