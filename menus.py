from settings import settings
from game import Game, PlayerType
from lang import lang
from util import getInput, toInt

class GreetingScreen:
    @staticmethod
    def run() -> None:
        Game.printTitle()
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
    NAME = lang.getMessage("playMenuName")

    @staticmethod
    def run() -> None:
        Game.printTitle()
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
            print(lang.getMessage("firstPlayerWrongInput", ", ".join(PlayerType.names())))
            firstPlayer = PlayerType.getByName(getInput(lang.getMessage("firstPlayerInput")).capitalize())

        game = Game(boardSize, shipsAmount, firstPlayer)
        game.getShipPlacements()
        game.placeMachineShips()
        game.play()

class StatsMenu:
    NAME = lang.getMessage("statsMenuName")

    @staticmethod
    def run() -> None:
        pass

class SettingsMenu:
    NAME = lang.getMessage("settingsMenuName")

    @staticmethod
    def run() -> None:
        pass

class MainMenu:
    MENUS = (PlayMenu, StatsMenu, SettingsMenu)
    MENU_NAMES = tuple(m.NAME for m in MENUS)
    MENUS_RANGE = range(len(MENUS))

    @staticmethod
    def run() -> None:
        Game.printTitle()
        for i in MainMenu.MENUS_RANGE:
            print(f"{i + 1}. {MainMenu.MENU_NAMES[i]}")
        print()

        menuName = getInput(lang.getMessage("selectMenu")).capitalize()
        menuInt = toInt(menuName)
        while (menuInt == None or not MainMenu.MENUS_RANGE.count(menuInt - 1)) and not MainMenu.MENU_NAMES.count(menuName):
            print(lang.getMessage("invalidMenu", ", ".join(map(
                lambda m: f"{m} ({MainMenu.MENU_NAMES.index(m) + 1})", MainMenu.MENU_NAMES
            ))))
            menuName = getInput(lang.getMessage("selectMenu")).capitalize()
            menuInt = toInt(menuName)

        menuIndex: int = menuInt - 1 if menuInt else MainMenu.MENU_NAMES.index(menuName)
        menu = MainMenu.MENUS[menuIndex]
        menu.run()
