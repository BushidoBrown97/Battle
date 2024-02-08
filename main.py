import random
class BoardOutException(Exception):
    pass

class BoardUsedException(Exception):
    pass
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
class Ship:
    def __init__(self, length, start_dot, direction):
        self.length = length
        self.start_dot = start_dot
        self.direction = direction
        self.lives = length

    def dots(self):
        ship_dots = []
        x, y = self.start_dot.x, self.start_dot.y
        for i in range(self.length):
            if self.direction == 0:
                ship_dots.append(Dot(x + i, y))
            elif self.direction == 1:
                ship_dots.append(Dot(x, y + i))
        return ship_dots
class Board:
    def __init__(self):
        self.board = [['O' for _ in range(6)] for _ in range(6)]
        self.ships = []
        self.alive_ships = 0

    def out(self, dot):
        return not (0 <= dot.x < 6 and 0 <= dot.y < 6)

    def add_ship(self, ship):
        for dot in ship.dots():
            if self.out(dot) or dot in self.ships:
                raise BoardOutException('Not enough space for the ship on the board')

        for dot in ship.dots():
            self.board[dot.y][dot.x] = '■'
            self.ships.append(dot)
        self.alive_ships += 1

    def contour(self, ship, verbose=False):
        near_dots = []
        for dot in ship.dots():
            for i in range(-1, 2):
                for j in range(-1, 2):
                    near_dot = Dot(dot.x + i, dot.y + j)
                    if not self.out(near_dot) and near_dot not in near_dots:
                        near_dots.append(near_dot)

        for near_dot in near_dots:
            x, y = near_dot.x, near_dot.y
            if 0 <= x < 6 and 0 <= y < 6 and self.board[y][x] == 'O':
                if verbose:
                    print(f'Cell {near_dot} is surrounded')
                self.board[y][x] = 'T'

    def __str__(self):
        result = ''
        for i in range(6):
            result += f'{i + 1} | '
            for j in range(6):
                cell = self.board[i][j]
                if cell == '■':
                    result += '■ '
                elif cell == 'T':
                    result += 'T '
                else:
                    result += 'O '
            result += '\n'
        result += '   1 2 3 4 5 6\n'
        return result

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException('Shot is out of bounds!')

        if self.board[dot.y][dot.x] == '■':
            self.board[dot.y][dot.x] = 'X'
            self.alive_ships -= 1
            return True
        elif self.board[dot.y][dot.x] == 'O':
            self.board[dot.y][dot.x] = 'T'
        else:
            raise BoardUsedException('Shot has already been made in this place!')
        return False
class Player:
    def __init__(self, own_board):
        self.own_board = own_board

    def ask(self):
        raise NotImplementedError("Asking for coordinates")

    def move(self, enemy_board, dot):
        repeat_move = False
        try:
            repeat_move = enemy_board.shot(dot)
        except BoardOutException as e:
            print(e)
        except BoardUsedException as e:
            print(e)
        return repeat_move
class AI(Player):
    def __init__(self, own_board):
        super().__init__(own_board)

    def ask(self):
        x = random.randint(0, 5)
        y = random.randint(0, 5)
        return Dot(x, y)


class User(Player):
    def __init__(self, own_board):
        super().__init__(own_board)

    def ask(self):
        while True:
            try:
                x = int(input("Enter the x coordinate: "))
                y = int(input("Enter the y coordinate: "))
                if 0 <= x <= 5 and 0 <= y <= 5:
                    return Dot(x, y)
                else:
                    print('Enter valid coordinates!')
            except ValueError:
                print('Try again!')
class Game:
    def __init__(self):
        self.player = None
        self.ai = None

    def random_board(self):
        player_board = Board()
        ai_board = Board()
        ship_lengths = [2, 3, 3, 4, 5]

        for board in [player_board, ai_board]:
            for length in ship_lengths:
                while True:
                    x = random.randint(0, 5)
                    y = random.randint(0, 5)
                    direction = random.choice([0, 1])
                    start_dot = Dot(x, y)
                    ship = Ship(length, start_dot, direction)
                    try:
                        board.add_ship(ship)
                        break
                    except BoardOutException:
                        continue

        self.player = User(player_board)
        self.ai = AI(ai_board)

    def greet(self):
        print('Welcome to Battleship!')
        print("Your board:")
        print(self.player.own_board)
        print("Computer's board:")
        print(self.ai.own_board)  # Добавляем вывод доски компьютера после вывода доски игрока

    def loop(self):
        while True:
            print("Player's turn...")
            player_dot = self.player.ask()
            repeat_move = self.player.move(self.ai.own_board, player_dot)
            print("Your board after player's move:")
            print(self.player.own_board)  # Вывод доски игрока после его хода
            print("Computer's board after player's move:")
            print(self.ai.own_board)  # Вывод доски компьютера после хода игрока

            if repeat_move:
                print("Player repeats the turn...")
            else:
                if self.ai.own_board.alive_ships == 0:
                    print("Player wins!")
                    break

            print("Computer's turn...")
            ai_dot = self.ai.ask()
            repeat_move = self.ai.move(self.player.own_board, ai_dot)
            print("Your board after computer's move:")
            print(self.player.own_board)  # Вывод доски игрока после хода компьютера
            print("Computer's board after computer's move:")
            print(self.ai.own_board)  # Вывод доски компьютера после его хода

            if repeat_move:
                print("Computer repeats the turn...")
            else:
                if self.player.own_board.alive_ships == 0:
                    print("Computer wins!")
                    break

    def start(self):
        self.random_board()
        self.greet()
        self.loop()




if __name__ == '__main__':
    game = Game()
    game.start()