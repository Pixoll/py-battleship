import enum
from random import randrange
from types import MappingProxyType
from typing import Any, Self
from util import center, clear, getInput, pause, toInt

class Enum(enum.Enum):
    _member_map_: dict[str, Self]
    _value2member_map_: dict[str, Self]
    @classmethod
    def members(cls) -> MappingProxyType[str, Self]:
        return cls.__members__
    @classmethod
    def names(cls) -> list[str]:
        return cls._member_names_
    @classmethod
    def getName(cls, index: int) -> str:
        return cls._member_names_[index]
    @classmethod
    def getRandom(cls) -> Self:
        names: list[str] = cls._member_names_
        index: int = randrange(len(names))
        return cls._member_map_[names[index]]
    @classmethod
    def getByValue(cls, value: Any) -> Self | None:
        return cls._value2member_map_.get(value)
    @classmethod
    def getByName(cls, name: str) -> Self | None:
        return cls.__members__.get(name)
    @classmethod
    def values(cls) -> list[Self]:
        return [x for x in cls.__members__.values()]

class IntEnum(enum.IntEnum, Enum):
    ""

class StrEnum(enum.StrEnum, Enum):
    ""

class ShipType(IntEnum):
    Empty = enum.auto(0)
    Patrol = enum.auto()
    Cruiser = enum.auto()
    Submarine = enum.auto()
    Battleship = enum.auto()
    Carrier = enum.auto()
    Hit = enum.auto()

ShipTypeRepr = (".", "P", "C", "S", "B", "A", "x")

class ShipOrientation(StrEnum):
    Horizontal = "H"
    Vertical = "V"

class PegType(IntEnum):
    Empty = enum.auto(0)
    Hit = enum.auto()
    Miss = enum.auto()

PegTypeRepr = (".", "H", "M")

class PlayerType(IntEnum):
    Human = enum.auto(0)
    Machine = enum.auto()

class Game:
    BoardSizeRange: range = range(10, 1001)
    ShipsAmountMin = 1
    Name = "Py Battleship"
    TitleLength = 100
    TitleText = "#" * TitleLength + "\n#" + center(Name, TitleLength - 2) + "#\n" + "#" * TitleLength + "\n"
    BoardsSeparation = 10

    @staticmethod
    def shipsAmountRange(N: int) -> range:
        return range(Game.ShipsAmountMin, N + 1)

    @staticmethod
    def printTitle() -> None:
        clear()
        print(Game.TitleText)

    def __init__(self, boardSize: int, shipsAmount: int, firstPlayer: PlayerType):
        self.boardSize: int = boardSize
        self.shipsAmount: int = shipsAmount
        self.firstPlayer: PlayerType = firstPlayer

        self.playerBoard: list[list[ShipType]] = []
        self.trackingBoard: list[list[PegType]] = []
        self.machineBoard: list[list[ShipType]] = []

        for i in range(boardSize):
            self.playerBoard.append([])
            self.machineBoard.append([])
            self.trackingBoard.append([])
            for _ in range(boardSize):
                self.playerBoard[i].append(ShipType.Empty)
                self.machineBoard[i].append(ShipType.Empty)
                self.trackingBoard[i].append(PegType.Empty)

        self.turn: PlayerType = firstPlayer

        boardDisplaySize: int = boardSize * 2 + 1
        self.boardsSeparator: str = " " * Game.BoardsSeparation
        self.boardDirectionIndicator: str = center(
            "  " + ("> " * boardSize).strip() + self.boardsSeparator + "  " + ("> " * boardSize).strip(),
            Game.TitleLength,
            includeRight = False
        )
        self.boardsTitles: str = center(
            center("Your board", boardDisplaySize)
            + self.boardsSeparator
            + center("Tracking board", boardDisplaySize),
            Game.TitleLength,
            includeRight = False
        ) + "\n"

        self.playerShipCells: int = 0
        self.machineShipCells: int = 0

    def __repr__(self) -> str:
        return f"Game({self.boardSize}, {self.shipsAmount}, PlayerType.{PlayerType.getName(self.firstPlayer)})"

    @property
    def currentBoard(self) -> list[list[ShipType]]:
        return self.playerBoard if self.turn == PlayerType.Human else self.machineBoard

    @property
    def turnName(self) -> str:
        return PlayerType.getName(self.turn)

    def getBoard(self, player: PlayerType) -> list[list[ShipType]]:
        return self.playerBoard if player == PlayerType.Human else self.machineBoard

    def isValidCoords(self, x: int, y: int) -> bool:
        return x >= 0 and x < self.boardSize and y >= 0 and y < self.boardSize

    def canPlaceShip(self, x: int, y: int, type: ShipType, orientation: ShipOrientation) -> bool:
        length: int = int(type)
        offset: int = int(length / 2)

        if orientation == ShipOrientation.Horizontal:
            beginX: int = x - offset
            if not self.isValidCoords(beginX, y):
                return False
            endX: int = beginX + length
            return self.isValidCoords(endX, y)
        else:
            beginY: int = y - offset
            if not self.isValidCoords(x, beginY):
                return False
            endY: int = beginY + length
            return self.isValidCoords(x, endY)

    def hasShip(self, x: int, y: int) -> bool:
        return self.currentBoard[x][y] != ShipType.Empty

    def placeShip(self, x: int, y: int, type: ShipType, orientation: ShipOrientation, player: PlayerType) -> None:
        length: int = int(type)
        offset: int = int(length / 2)
        board: list[list[ShipType]] = self.getBoard(player)

        if player == PlayerType.Human:
            self.playerShipCells += length
        else:
            self.machineShipCells += length

        if orientation == ShipOrientation.Horizontal:
            start: int = x - offset
            for i in range(length):
                board[start + i][y] = type
        else:
            start: int = y - offset
            for i in range(length):
                board[x][start + i] = type

    def placeMachineShips(self) -> None:
        placed: int = 0
        while placed < self.shipsAmount:
            x: int = randrange(self.boardSize)
            if not self.isValidCoords(x, 0):
                continue
            y: int = randrange(self.boardSize)
            orientation: ShipOrientation = ShipOrientation.getRandom()
            if not self.isValidCoords(x, y) or not self.canPlaceShip(x, y, ShipType.Submarine, orientation):
                continue
            self.placeShip(x, y, ShipType.Submarine, orientation, PlayerType.Machine)
            self.machineBoard[x][y] = ShipType.Submarine
            placed += 1

    def getShipPlacement(self, i: int) -> tuple[int, int, ShipType, ShipOrientation]:
        type: ShipType = ShipType.Submarine
        while True:
            raw = getInput(f"Enter ship #{i} position and orientation (format: x, y, H|V): ").split()
            if len(raw) != 3:
                print("Invalid format, try again")
                continue

            x: int | None = toInt(raw[0])
            y: int | None = toInt(raw[1])
            orientation: ShipOrientation | None = ShipOrientation.getByValue(raw[2].upper())

            if x == None or y == None or not self.isValidCoords(x - 1, y - 1):
                print("Invalid x or y, try again")
                continue
            x -= 1
            y -= 1
            if orientation == None:
                print("Invalid orientation value, try again")
                continue
            if not self.canPlaceShip(x, y, type, orientation):
                print("Can't place a ship here, try again")
                continue

            return (x, y, type, orientation)

    def getShipPlacements(self) -> None:
        Game.printTitle()
        print(f"Coordinates must be within the range [1, {self.boardSize}]")
        print(f"Orientation must be either {', '.join(map(
            lambda a: f'or {a}' if ShipOrientation.values()[-1] == a else a,
            ShipOrientation.values()
        ))}")

        for i in range(self.shipsAmount):
            [x, y, type, orientation] = self.getShipPlacement(i + 1)
            self.placeShip(x, y, type, orientation, PlayerType.Human)

    def display(self, turn: bool = True) -> None:
        Game.printTitle()
        print(self.boardsTitles)

        for i in reversed(range(self.boardSize)):
            line: str = "^ "
            for j in range(self.boardSize):
                line += ShipTypeRepr[self.playerBoard[j][i]] + " "
            line = line.rstrip()
            line += self.boardsSeparator + "^ "
            for j in range(self.boardSize):
                line += PegTypeRepr[self.trackingBoard[j][i]] + " "
            print(center(line.rstrip(), Game.TitleLength, includeRight = False))
        print(self.boardDirectionIndicator)

        print()
        if turn:
            print(center(f"{self.turnName}'s turn", Game.TitleLength, includeRight = False))
            print()

    def getShotTarget(self) -> bool:
        while True:
            raw = getInput("Enter where do you want to shoot (x, y): ").split()
            if len(raw) != 2:
                print("Invalid format, try again")
                continue

            x: int | None = toInt(raw[0])
            y: int | None = toInt(raw[1])
            if x == None or y == None or not self.isValidCoords(x - 1, y - 1):
                print("Invalid x or y, try again")
                continue

            x -= 1
            y -= 1
            if self.machineBoard[x][y] == ShipType.Hit:
                print("You already shot here")
                continue

            machineShip: ShipType = self.machineBoard[x][y]
            miss: bool = machineShip == ShipType.Empty
            print("Miss!" if miss else "Hit! You get another turn")

            if not miss:
                self.machineShipCells -= 1

            self.machineBoard[x][y] = ShipType.Hit
            self.trackingBoard[x][y] = PegType.Miss if miss else PegType.Hit
            return not miss

    def shootAtHuman(self) -> bool:
        while True:
            x: int = randrange(self.boardSize)
            if not self.isValidCoords(x, 0):
                continue
            y: int = randrange(self.boardSize)
            if not self.isValidCoords(x, y) or self.playerBoard[x][y] == ShipType.Hit:
                continue

            print(f"Machine shoots at ({x + 1}, {y + 1})")
            playerShip: ShipType = self.playerBoard[x][y]
            miss: bool = playerShip == ShipType.Empty
            print("Miss!" if miss else "Hit! The machine gets another turn")

            if not miss:
                self.playerShipCells -= 1
            self.playerBoard[x][y] = ShipType.Hit
            return not miss

    def play(self) -> None:
        while self.playerShipCells and self.machineShipCells:
            self.display()
            anotherTurn: bool
            if self.turn == PlayerType.Human:
                anotherTurn = self.getShotTarget()
            else:
                anotherTurn = self.shootAtHuman()
            if not anotherTurn:
                self.turn = PlayerType.Human if self.turn == PlayerType.Machine else PlayerType.Machine
            pause()

        self.display(False)
        print(center(
            f"{'Human' if self.playerShipCells else 'Machine'} wins!",
            Game.TitleLength,
            includeRight = False
        ))
        print()
