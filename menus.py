from settings import settings
from game import Game, PlayerType
from lang import lang
from util import getInput, toInt

class GreetingScreen:
    @staticmethod
    def run() -> None:
        language = getInput(lang.getMessage("langInput"))
        while not (language in lang.getLangs()) and not (language.capitalize() in lang.getLangNames()):
            print(lang.getMessage("langWrongInput", ", ".join(map(
                lambda l: f"{lang.getLangName(l)} ({l})", lang.getLangs()
            ))))
            language = getInput(lang.getMessage("langInput"))

        if not (language in lang.getLangs()):
            language = lang.getLangId(language.capitalize())

        lang.setLang(language)
        settings.setValue("firstLaunch", False)
        Game.printTitle()

class PlayMenu:
    NAME = "Play"

    @staticmethod
    def run() -> None:
        boardSize = toInt(getInput(lang.getMessage("boardSizeInput")))
        while boardSize == None or not Game.BOARD_SIZE_RANGE.count(boardSize):
            print(lang.getMessage("boardSizeWrongInput", min(Game.BOARD_SIZE_RANGE), max(Game.BOARD_SIZE_RANGE)))
            boardSize = toInt(getInput(lang.getMessage("boardSizeInput")))

        shipsAmountRange = Game.shipsAmountRange(boardSize)
        shipsAmount = toInt(getInput(lang.getMessage("shipsAmountInput")))
        while shipsAmount == None or not shipsAmountRange.count(shipsAmount):
            print(lang.getMessage("shipsAmountWrongInput", min(shipsAmountRange), max(shipsAmountRange)))
            shipsAmount = toInt(getInput(lang.getMessage("shipsAmountInput")))

        firstPlayer = PlayerType.getByName(getInput(lang.getMessage("firstPlayerInput")).capitalize())
        while firstPlayer == None:
            print(lang.getMessage("firstPlayerWrongInput", ", ".join(map(
                lambda a: f"or {a}" if PlayerType.names()[-1] == a else a, PlayerType.names()
            ))))
            firstPlayer = PlayerType.getByName(getInput(lang.getMessage("firstPlayerInput")).capitalize())

        game = Game(boardSize, shipsAmount, firstPlayer)
        game.getShipPlacements()
        game.placeMachineShips()
        game.play()

class StatsMenu:
    NAME = "Stats"

    @staticmethod
    def run() -> None:
        pass

class SettingsMenu:
    NAME = "Settings"

    @staticmethod
    def run() -> None:
        pass

class MainMenu:
    MENUS = (PlayMenu, StatsMenu, SettingsMenu)

    @staticmethod
    def run() -> None:
        for i in range(len(MainMenu.MENUS)):
            print(f"{i + 1}. {MainMenu.MENUS[i].NAME}")
