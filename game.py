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

    class Ship:
        def __init__(self, x: int, y: int, type: ShipType, orientation: ShipOrientation):
            self.type: ShipType = type
            self.orientation: ShipOrientation = orientation

            length: int = int(type)
            offset: int = int(length / 2)

            self.coords: list[tuple[int, int]] = []
            self.hits: list[bool] = []
            self.destroyed = False
            self.untilDestroyed = length

            if orientation == ShipOrientation.Horizontal:
                start: int = x - offset
                for i in range(length):
                    self.coords.append((start + i, y))
            else:
                start: int = y - offset
                for i in range(length):
                    self.coords.append((x, start + i))

            for i in range(length):
                self.hits.append(False)

        def setHit(self, x: int, y: int) -> None:
            index: int = self.coords.index((x, y))
            self.hits[index] = True
            self.untilDestroyed -= 1
            if self.untilDestroyed == 0:
                self.destroyed = True

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

        self.playerShips: list[Game.Ship] = []
        self.machineShips: list[Game.Ship] = []

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

    def getShips(self, player: PlayerType) -> list[Ship]:
        return self.playerShips if player == PlayerType.Human else self.machineShips

    def isValidCoords(self, x: int, y: int) -> bool:
        return x >= 0 and x < self.boardSize and y >= 0 and y < self.boardSize

    def canPlaceShip(self, ship: Ship) -> bool:
        for x, y in ship.coords:
            if not self.isValidCoords(x, y):
                return False
        return True

    def hasShip(self, x: int, y: int) -> bool:
        return self.currentBoard[x][y] != ShipType.Empty

    def getShip(self, x: int, y: int, player: PlayerType) -> Ship | None:
        for ship in self.getShips(player):
            try:
                ship.coords.index((x, y))
                return ship
            except:
                continue
        return None

    def placeShip(self, ship: Ship, player: PlayerType) -> None:
        length: int = int(ship.type)
        if player == PlayerType.Human:
            self.playerShipCells += length
        else:
            self.machineShipCells += length

        board: list[list[ShipType]] = self.getBoard(player)
        for x, y in ship.coords:
            board[x][y] = ship.type

    def placeMachineShips(self) -> None:
        placed: int = 0
        while placed < self.shipsAmount:
            x: int = randrange(self.boardSize)
            if not self.isValidCoords(x, 0):
                continue
            y: int = randrange(self.boardSize)
            orientation: ShipOrientation = ShipOrientation.getRandom()
            ship: Game.Ship = Game.Ship(x, y, ShipType.Submarine, orientation)

            if not self.isValidCoords(x, y) or not self.canPlaceShip(ship):
                continue

            self.placeShip(ship, PlayerType.Machine)
            self.getShips(PlayerType.Machine).append(ship)
            self.machineBoard[x][y] = ShipType.Submarine
            placed += 1

    def createShip(self, i: int) -> Ship:
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

            ship: Game.Ship = Game.Ship(x, y, type, orientation)
            if not self.canPlaceShip(ship):
                print("Can't place a ship here, try again")
                continue

            return ship

    def getShipPlacements(self) -> None:
        Game.printTitle()
        print(f"Coordinates must be within the range [1, {self.boardSize}]")
        print(f"Orientation must be either {', '.join(map(
            lambda a: f'or {a}' if ShipOrientation.values()[-1] == a else a,
            ShipOrientation.values()
        ))}")

        for i in range(self.shipsAmount):
            ship: Game.Ship = self.createShip(i + 1)
            self.placeShip(ship, PlayerType.Human)
            self.getShips(PlayerType.Human).append(ship)

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

            ship: Game.Ship | None = self.getShip(x, y, PlayerType.Machine)
            miss: bool = ship == None
            if miss:
                print("Miss!")
            else:
                ship.setHit(x, y)
                print(("Sunk! " if ship.destroyed else "Hit! ") + "You get another turn")

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
            ship: Game.Ship | None = self.getShip(x, y, PlayerType.Human)
            miss: bool = ship == None
            if miss:
                print("Miss!")
            else:
                ship.setHit(x, y)
                print(("Sunk! " if ship.destroyed else "Hit! ") + "The machine gets another turn")

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
