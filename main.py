from game import Game, PlayerType
from lang import lang
from util import close, getInput, toInt

def main():
    Game.printTitle()

    boardSize = toInt(getInput(lang.getMessage("boardSizeInput")))
    while not boardSize or not Game.BOARD_SIZE_RANGE.count(boardSize):
        print(lang.getMessage("boardSizeWrongInput", min(Game.BOARD_SIZE_RANGE), max(Game.BOARD_SIZE_RANGE)))
        boardSize = toInt(getInput(lang.getMessage("boardSizeInput")))

    shipsAmountRange = Game.shipsAmountRange(boardSize)
    shipsAmount = toInt(getInput(lang.getMessage("shipsAmountInput")))
    while not shipsAmount or not shipsAmountRange.count(shipsAmount):
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

    close(0)

if __name__ == "__main__":
    main()
