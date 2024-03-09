import random
import time
import os
import keyboard
import threading

class Tetris:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.board = [[' ' for _ in range(width)] for _ in range(height)]
        self.current_piece = self.new_piece()
        self.score = 0
        self.game_over = False

    def new_piece(self):
        pieces = [
            [['#', '#'],
             ['#', '#']],
            [['#', '#', '#', '#']],
            [[' ', '#', ' '],
             ['#', '#', '#']],
            [['#', ' ', ' '],
             ['#', '#', '#']],
            [[' ', ' ', '#'],
             ['#', '#', '#']],
            [[' ', '#', '#'],
             ['#', '#', ' ']],
            [['#', '#', ' '],
             [' ', '#', '#']]
        ]
        return random.choice(pieces)

    def move_piece_down(self):
        self.current_piece_y += 1
        if self.collides():
            self.current_piece_y -= 1
            self.merge_piece()
            self.current_piece = self.new_piece()
            self.current_piece_x = self.width // 2 - len(self.current_piece[0]) // 2
            self.current_piece_y = 0
            if self.collides():
                self.game_over = True

    def move_piece_left(self):
        self.current_piece_x -= 1
        if self.collides():
            self.current_piece_x += 1

    def move_piece_right(self):
        self.current_piece_x += 1
        if self.collides():
            self.current_piece_x -= 1

    def rotate_piece(self):
        self.current_piece = list(zip(*self.current_piece[::-1]))
        if self.collides():
            self.current_piece = list(zip(*self.current_piece[::-1]))

    def merge_piece(self):
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[0])):
                if self.current_piece[y][x] == '#':
                    self.board[self.current_piece_y + y][self.current_piece_x + x] = '#'

    def collides(self):
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[0])):
                if self.current_piece[y][x] == '#' and \
                        (self.current_piece_y + y >= self.height or
                         self.current_piece_x + x < 0 or
                         self.current_piece_x + x >= self.width or
                         self.board[self.current_piece_y + y][self.current_piece_x + x] == '#'):
                    return True
        return False

    def check_lines(self):
        lines_to_clear = []
        for y in range(self.height):
            if all(cell == '#' for cell in self.board[y]):
                lines_to_clear.append(y)
        if lines_to_clear:
            self.score += len(lines_to_clear) * 100
            for line in lines_to_clear:
                del self.board[line]
                self.board.insert(0, [' ' for _ in range(self.width)])

    def display(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Score:', self.score)
        for y in range(self.height):
            for x in range(self.width):
                if x >= self.current_piece_x and x < self.current_piece_x + len(self.current_piece[0]) and \
                   y >= self.current_piece_y and y < self.current_piece_y + len(self.current_piece):
                    if self.current_piece[y - self.current_piece_y][x - self.current_piece_x] == '#':
                        print('#', end=' ')
                    else:
                        print(self.board[y][x], end=' ')
                else:
                    print(self.board[y][x], end=' ')
            print()
        print('Press Q to quit')

    def handle_input(self):
        while not self.game_over:
            if keyboard.is_pressed('q'):
                self.game_over = True
            elif keyboard.is_pressed('a'):
                self.move_piece_left()
            elif keyboard.is_pressed('d'):
                self.move_piece_right()
            elif keyboard.is_pressed('s'):
                self.move_piece_down()
            elif keyboard.is_pressed('r'):
                self.rotate_piece()
            time.sleep(0.1)  # Добавим небольшую задержку для снижения нагрузки на процессор

    def run(self):
        input_thread = threading.Thread(target=self.handle_input)
        input_thread.start()
        while not self.game_over:
            self.current_piece_x = self.width // 2 - len(self.current_piece[0]) // 2
            self.current_piece_y = 0
            while not self.game_over:
                self.display()
                self.move_piece_down()
                if self.collides():
                    break
                self.check_lines()
                time.sleep(0.5)
        input_thread.join()
        print('Game over! Your score:', self.score)

if __name__ == "__main__":
    tetris = Tetris()
    tetris.run()
