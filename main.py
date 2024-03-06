from game import Game, PlayerType
from util import close, getInput, toInt

def main():
    Game.printTitle()

    boardSize = toInt(getInput("Enter the board size: "))
    while not boardSize or not Game.BOARD_SIZE_RANGE.count(boardSize):
        print(f"Board size must be in range [{min(Game.BOARD_SIZE_RANGE)}, {max(Game.BOARD_SIZE_RANGE)}]")
        boardSize = toInt(getInput("Enter the board size: "))

    shipsAmountRange = Game.shipsAmountRange(boardSize)
    shipsAmount = toInt(getInput("Enter the ships amount: "))
    while not shipsAmount or not shipsAmountRange.count(shipsAmount):
        print(f"Ships amount must be in range [{min(shipsAmountRange)}, {max(shipsAmountRange)}]")
        shipsAmount = toInt(getInput("Enter the ships amount: "))

    firstPlayer = PlayerType.getByName(getInput("Enter who starts first: ").capitalize())
    while firstPlayer == None:
        print(f"First player must be either {', '.join(map(
            lambda a: f'or {a}' if PlayerType.names()[-1] == a else a, PlayerType.names()
        ))}")
        firstPlayer = PlayerType.getByName(getInput("Enter who starts first: ").capitalize())

    game = Game(boardSize, shipsAmount, firstPlayer)
    game.getShipPlacements()
    game.placeMachineShips()
    game.play()

    close(0)

if __name__ == "__main__":
    main()
