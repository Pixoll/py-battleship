from os import listdir
from typing import Any

class Lang:
    LANG_FOLDER = "./lang/"

    def __init__(self) -> None:
        self.lang = "en"
        self.langs: dict[str, dict[str, str]] = {}

        for file in listdir(Lang.LANG_FOLDER):
            lang: str = file.split(".")[0]
            langMessages: dict[str, str] = {}
            for line in open(Lang.LANG_FOLDER + file, encoding = "utf-8"):
                if not len(line.strip()) or line.startswith("#"):
                    continue
                [key, value] = line.split("=", 1)
                langMessages[key] = value.replace("\n", "").replace("''", "'")
            self.langs[lang] = langMessages

    def getLangs(self) -> list[str]:
        return [l for l in self.langs.keys()]

    def getLangNames(self) -> list[str]:
        return [l["langName"] for l in self.langs.values()]

    def getLangName(self, id: str) -> str:
        return self.langs[id]["langName"]

    def getMessage(self, key: str, *args: Any) -> str:
        value: str = self.langs[self.lang][key]
        if not len(args):
            return value
        for i in range(len(args)):
            value = value.replace(f"{{{i}}}", str(args[i]))
        return value

lang = Lang()
