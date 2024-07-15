#2048
import random
from tkinter import *


# define grid object 
class Grid: 
    def  __init__(self, init_layout = 
                [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]], num_start = 3): 
        self.grid = self.init_grid(init_layout)
        # randomly adds num_start (defualt 3) starting values
        # can also take a different initial state if you want to do a challenge or something 
        for _ in range(num_start): 
            self.replenish() 

    # defines move left, using the __add__ implimentation for Spaces found in the space class.
    # starts from the right and moves left, adding each square to its rightmost neighbor 
    # NOTE repeats 3 times to avoid some edge cases like [0, 4, 8, 16] where without repeats it results in [4, 0, 8, 16]
    # this can get generalized for any board size and/ or optimized 
    def move_left(self): 
        for _ in range(len(self.grid) - 1):
            for row in self.grid: 
                for i in range(len(row), -1, -1): 
                    if i + 1 < len(row):
                        row[i] + row[i + 1]
        self.replenish()
                    
    # all other moves rotate and, move left, rotate back 
    def move_right(self):
        self.rotate_grid(2)
        self.move_left()
        self.rotate_grid(2)

    def move_down(self): 
        self.rotate_grid(1)
        self.move_left() 
        self.rotate_grid(3)

    def move_up(self): 
        self.rotate_grid(3)
        self.move_left() 
        self.rotate_grid(1)

    # prints readably
    def display(self): 
        for row in self.grid:
            print(row)

    # creates an array of Space classes instead of an array of integers
    def init_grid(self, init_layout): 
        #takes 2d array 
        out = [] 
        for row in init_layout: 
            cur =  [] 
            for val in row: 
                cur.append(Space(val))
            out.append(cur)
        return out
    
    # impliments rotate 'i' (will rotate input number of times)
    # for use in all moves other than move left 
    def rotate_grid(self, i):
        for _ in range(i):
            self.grid = [[*t] for t in zip(*self.grid[::-1])]

    # adds new value (2 or 4) to a random tile with 0 value 
    def replenish(self): 
        blank = [] 
        for row in self.grid: 
            for column in row: 
                if column.val == 0: 
                    blank.append(column)

        random.choice(blank).new_val()
    
    # Checks if player has lost 
    def is_lose_state(self): 
        no_zero = True
        for row in self.grid: 
            for column in row: 
                if column.val == 0: 
                    no_zero = False
        return no_zero
    
    # gets score values from each tile
    # NOTE Bug: score starts at 1 for unknown reason 
    def get_score(self): 
        score = True
        for row in self.grid: 
            for column in row: 
                score += column.score
        return score
    
    # refreshes all Space's, to be used at the end of each move
    def refresh(self): 
        for row in self.grid: 
            for column in row: 
                column.refresh()

    


# impliments space class for use in grid 
class Space: 
    def __init__(self, val):
        self.val = val 
        self.score = 0 
        self.can_combine = True

    # + implimentation for use in moves 
    def __add__(self, other):
        if (self.val == other.val) and (self.can_combine and other.can_combine): 
            self.val = self.val + other.val 
            other.delete() 
            self.score += self.val 
            self.can_combine = False
        elif self.val == 0: 
            self.val = other.val 
            other.delete() 

    # sets value to 0, used during moves 
    def delete(self): 
        self.val = 0 

    # just makes it print
    def __repr__(self): 
        return str(self.val)
    
    def __str__(self):
        return str(self.val)
    
    # for use when replinishing board 
    def new_val(self): 
        assert(self.val == 0)
        self.val = random.choice([2, 4])

    # boolian utility function 
    def is_zero(self):
        return self.val == 0 
    
    # refreshes can_combine at the end of a given turn 
    def refresh(self): 
        self.can_combine = True


# impliments game using grid 
class Game(): 
    def __init__(self, starting_grid=None, num_start=3, blank_grid_size=None): 
        if blank_grid_size is not None: 
            starting_grid = [([0] * blank_grid_size)] * blank_grid_size
            print(starting_grid)
        if starting_grid is not None: 
            self.grid = Grid(starting_grid, num_start) 
        else: 
            self.grid = Grid(num_start=num_start)
        self.highscore = 0 
        self.turn_count = 0 

    # loops, gives io for each turn 
    def play_game(self): 
        print("Legal plays: left (l), right (r), up (u), down (d)")
        while(True): 
            self.grid.display()
            print("score: " + str(self.highscore))
            print("turn: " + str(self.turn_count))
            if self.grid.is_lose_state(): 
                print("You Lose")
                break 
            play = input()
            # in newer versions of python this should be handled with a case switch rather than a series of if's, I'm running a older version of python tho
            if play == "l":
                self.grid.move_left()
                self.turn_count += 1 
            elif play == "r":
                self.grid.move_right()
                self.turn_count += 1 
            elif play == "u": 
                self.grid.move_up()
                self.turn_count += 1 
            elif play == "d": 
                self.grid.move_down()
                self.turn_count += 1 
            else: 
                print("illegal move, legal move are l, r, u, and d")
            self.highscore = self.grid.get_score() 
            self.grid.refresh()

# main function 
def main():
    game = Game(blank_grid_size=4)
    game.play_game()

if __name__ == "__main__": 
    main() 

