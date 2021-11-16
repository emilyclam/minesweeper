"""
This might be ambitious but I want to make minesweeper!
Also I want to try making this with correct conventions so that there's still a green check^

now:
X board w/ logical grid (make a class)
X selecting a square: outline the border of the square; controlled through keypresss
X presetting the locations of the bombs
X finding if a square is a number (and if so, what?) or gray space; draw it under the square
X keypress functions: flag and uncover (f and space)
    X flag graphic
    X check if there's a large chunk
    X check if it's a bomb
    X check if win (separate method)
X check if win: all bombs are flagged or all squares are uncovered

extra:
- difficulty settings (size of board)

^I'm too lazy to do that nvm

"""

"""
remaining things:
X a lose state (so far bombs don't really do anything)
X when a num square has been flagged and then unflagged, and then uncovered, the background stays the light gray color
X when all the tiles are uncovered (but not all flags been done) the game doesn't say that you win
X display a counter of how many bombs there are total and how many flags (including incorrect ones) you've done
X CHANGE THE COLORS! IT'S hard to see the dark colors against the dark gray after you open it. i don't need to 
cause additional eye strain... (especially 2/green...) --> make them lighter colors?
X make it so when it's uncovered you can't flag it
X if something is already flagged, "opening it" will just take away the flag

"""

"""
I know I said I wanted ths to be warning free, but I'm too lazy to make all my for loops have different variables so meh 
"""

import turtle
import random
import time

# board constants
w = 500
h = 400
"""
on a/my full screen, row=15 and col=40 are the highest dimensions, because I don't feel like fixing the size variable
"""
row = 15
col = 40

size = 15
border_size = 10  # it's best not to change SIZE and BORDER_SIZE ...
board_width = col*(size+border_size) - border_size
board_height = row*(size+border_size) - border_size
board_top_edge = board_height//2
board_left_edge = -(board_width//2)

# value variables
num_bombs = row*col//10
sqs = []  # array to hold squares
# colors = ["blue", "green", "red", "midnightblue", "maroon", "darkolivegreen", "goldenrod", "powderblue"]
colors = ["deepskyblue", "palegreen", "lightcoral", "gold"]
correct_flags = 0
flag_count = 0
uncovered_tiles = 0
game_state = "playing"  # either "playing" "lose" or "win"
# note: you win when
#   a) correct_flags = num_bombs = len(bombs)
#   b) uncovered_tiles = len(sqs) - num_bombs

wn = turtle.Screen()
wn.bgcolor("darkslategrey")
wn.title("Minesweeper by LEM")
wn.setup(w, h)
wn.tracer(0)

txt = turtle.Turtle()
txt.hideturtle()
txt.color("white")
txt.pu()
txt.goto(0, board_top_edge + 30)
txt.write("m i n e s w e e p e r", False, align="center", font=("Bahnschrift", 20, "normal"))

class Square(turtle.Turtle):
    def __init__(self, x, y, value):
        super(Square, self).__init__()
        self.x = x
        self.y = y
        self.value = value  # "bomb", 1-8, 0 (blank)
        self.is_opened = False  # Whether it was clicked or not
        self.is_flagged = False
        self.speed = 0

    def make_square(self):
        # Makes a squares and randomly assigns bomb
        self.pu()
        self.hideturtle()
        self.goto(self.x, self.y)
        self.shape("square")

        if self.is_opened:
            # all things opened have a dark gray background
            self.color("dimgrey")
            self.stamp()

            global uncovered_tiles
            uncovered_tiles += 1

            # draws the specific value
            if self.is_flagged:
                print("you used space to unflag")
                self.is_opened = False
                self.flag()
            elif self.value == "bomb":
                global game_state
                game_state = "lose"
                # only the bomb that you clicked gets a red background
                self.color("red")
                self.stamp()

                # draws all of the bombs
                for i in bombs:
                    #print("izza bomb!")
                    i.color("black")
                    i.penup()
                    i.shape("circle")
                    i.stamp()
            elif self.value > 0:
                # draw the number in its specific color
                c = colors[self.value - 1]
                self.pencolor(c)
                self.goto(self.x, self.y - (size + border_size) / 2)
                self.pendown()
                self.write(self.value, False, align="center", font=("courier new", 15, "bold"))
            else:
                # chunk-opening blank squares
                for i in sqs:
                    if not i.is_opened and self.distance(i) <= size+border_size:
                        i.is_opened = True
                        i.make_square()

            check_game()
        # draws a light, covered tile
        else:
            self.color("grey")
            self.stamp()

    def open(self):  # this function gets called when space bar is hit
        # reveal square num/blank/bomb
        if not cs.is_opened:
            cs.is_opened = True  # only open if it was covered
            cs.make_square()  # redraws the square

    def flag(self):
        global correct_flags
        global flag_count
        # if it was already flagged, unflag it
        if cs.is_flagged:
            # have to reset the self attributes that were changed for the flagging
            cs.goto(cs.x, cs.y)
            cs.color("grey")
            cs.shapesize(stretch_wid=1, stretch_len=1)
            cs.stamp()
            cs.is_flagged = False
            flag_count -= 1
            if cs.value == "bomb":
                correct_flags -= 1
        elif not cs.is_flagged and not cs.is_opened:
            flag_count += 1
            if cs.value == "bomb":
                correct_flags += 1
            cs.is_flagged = True
            cs.draw_flag()
        track_progress()
        check_game()



    def draw_flag(self):
        self.goto(self.x+size/5, self.y+size/4)
        self.shapesize(stretch_len=.5, stretch_wid=0.3)
        self.color("red")
        self.stamp()

        self.goto(self.x-size/4, self.y)
        self.shape("square")
        self.shapesize(stretch_len=0.1, stretch_wid=.7)
        self.color("black")
        self.stamp()


def check_game():  # checks if you've won or lost after every move
    txt.goto(0, board_top_edge - board_height - 60)  # win/lose is written in same spot
    global game_state
    if game_state == "lose":
        txt.write("Y O U  L O S E !", False, align="center", font=("Consolas", 20, "bold"))

    elif correct_flags == num_bombs or uncovered_tiles == len(sqs) - num_bombs:
        game_state = "win"
        for i in range(3):
            txt.color("white")
            txt.write("Y O U  W O N !", False, align="center", font=("Consolas", 20, "bold"))
            time.sleep(.5)
            txt.undo()
            txt.color("darkslategrey")
            txt.write("Y O U  W O N !", False, align="center", font=("Consolas", 20, "bold"))
            time.sleep(.5)
            txt.undo()
        txt.color("white")
        txt.write("Y O U  W O N !", False, align="center", font=("Consolas", 20, "bold"))


def track_progress():
    tracker = turtle.Turtle()
    tracker.hideturtle()
    tracker.penup()
    tracker.speed(0)

    y = board_top_edge + 45
    x1 = -170
    x2 = 170
    tracker.sety(y)

    # draw the rectangles for them
    tracker.color("gray")
    tracker.shape("square")
    tracker.shapesize(stretch_len=2, stretch_wid=1.5)
    tracker.setx(x1)
    tracker.stamp()
    tracker.setx(x2)
    tracker.stamp()
    tracker.color("maroon")
    tracker.sety(y-10)

    # left: how many flags you've done
    tracker.setx(x1)
    tracker.write(flag_count, False, align="center", font=("Consolas", 15, "normal"))

    # right: how many flags there are remaining
    tracker.setx(x2)
    tracker.write(num_bombs - flag_count, False, align="center", font=("Consolas", 15, "normal"))


# Draws the squares
for y in range(row):
    for x in range(col):
        sqs.append(Square(board_left_edge + x*(size+border_size), board_top_edge - y*(size+border_size), 0))
        sqs[-1].make_square()
cs = sqs[0]  # cs = current_square

# decides bombs
bombs = random.sample(sqs, k=num_bombs)
for i in bombs:
    i.value = "bomb"

# finds values of other squares
for i in sqs:
    for j in bombs:
        if i.value != "bomb":
            if j.distance(i.x, i.y) < (size + border_size) * 2:
                i.value += 1


selector = turtle.Turtle()
# note that the squares.x are based on the center, while the selector is drawn from the top left corner
selector.x = board_left_edge - (size+border_size) // 2
selector.y = board_top_edge + (size+border_size) // 2
selector.speed(0)
selector.hideturtle()

# selector "methods"
# Draws the yellow selector square
def draw():
    selector.clear()
    selector.pensize(3)
    selector.penup()
    selector.goto(selector.x, selector.y)
    selector.pendown()
    selector.pencolor("yellow")

    for i in range(4):
        selector.forward(size+border_size)
        selector.right(90)


# matches selector location with it's square, and then returns that square object
def return_sq():
    # in the selector code size//2 uses // so this one has to too
    x = int(selector.x + size//2 + border_size/2)
    y = int(selector.y - size//2 - border_size/2)

    for i in sqs:
        if i.x == x and i.y == y:
            global cs
            cs = i


def move_up():
    # prevents selector from moving above the squares grid
    if selector.y < board_top_edge:
        selector.y += size + border_size
        return_sq()


def move_down():
    # remember that the selector.y is found at the top right corner.
    if selector.y > board_top_edge - board_height + size + border_size*2:
        selector.y -= size + border_size
        return_sq()


def move_left():
    if selector.x > board_left_edge:
        selector.x -= size + border_size
        return_sq()


def move_right():
    if selector.x < board_left_edge + board_width - size - border_size*2:
        selector.x += size + border_size
        return_sq()


# map of board console
for i in range(row*col):
    if sqs[i].value == "bomb":
        print("*", end=" ")
    else:
        print(sqs[i].value, end=" ")
    if (i+1) % col == 0:
        print("")
track_progress()

wn.listen()
wn.onkeypress(move_up, "w")
wn.onkeypress(move_down, "s")
wn.onkeypress(move_left, "a")
wn.onkeypress(move_right, "d")
wn.onkeypress(cs.open, "space")
wn.onkeypress(cs.flag, "f")


while True:
    wn.update()
    if game_state == "playing":
        draw()

wn.mainloop()
