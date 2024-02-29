from game import Game, PlayerType
from util import close, getInput, toInt

def main():
    Game.printTitle()

    boardSize = toInt(getInput("Enter the board size: "))
    if not boardSize or not Game.BoardSizeRange.count(boardSize):
        print(f"Board size must be in range [{min(Game.BoardSizeRange)}, {max(Game.BoardSizeRange)}]")
        close(1)

    shipsAmountRange = Game.shipsAmountRange(boardSize)
    shipsAmount = toInt(getInput("Enter the ships amount: "))
    if not shipsAmount or not shipsAmountRange.count(shipsAmount):
        print(f"Ships amount must be in range [{min(shipsAmountRange)}, {max(shipsAmountRange)}]")
        close(1)

    firstPlayer = PlayerType.getByName(getInput("Enter who starts first: ").capitalize())
    if firstPlayer == None:
        print(f"First player must be either {', '.join(map(
            lambda a: f'or {a}' if PlayerType.names()[-1] == a else a, PlayerType.names()
        ))}")
        close(1)

    game = Game(boardSize, shipsAmount, firstPlayer)
    game.getShipPlacements()
    game.placeMachineShips()
    game.play()

    close(0)

if __name__ == "__main__":
    main()
