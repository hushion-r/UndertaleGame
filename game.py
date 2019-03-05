""" ======================================================================
Author: Rae
Base from COMP123 HW6

"""

# -----------------

import random
from tkinter import *
import time


# =========================================================================

class WallGUI:
    """Draws a GUI window with a title label, a quit button, and a canvas with a green
    backdrop. The canvas responds to mouse clicks with the moveToward callback function.
    The Quit button responds to clicks with the doQuit callback function.
    This program allows the user to move a rectangle around"""

    def __init__(self):
        self.CANVAS_WIDTH = 600
        self.CANVAS_HEIGHT = 400
        self.BOARD_LENGTH = 6

        self.START_BOARD_X = 120
        self.START_BOARD_Y = 20
        self.TILE_SIZE = 60
        self.COLOURS = ["red", "yellow", "green", "orange", "blue", "purple", "pink"]
        self.SEND_BACK_COMMANDS = ("stop", "electrocution", "piranhas")

        self.MAIN_WIN = Tk()
        self.MAIN_WIN.title("Undertale Tile Game")

        self.TITLE_LABEL = Label(self.MAIN_WIN, text="Undertale Tile Game",
                                 font="Arial 20 bold", relief=GROOVE,
                                 justify=CENTER, bd=5)
        self.TITLE_LABEL.grid(row=0, column=1, padx=10, pady=10)

        self.QUIT_BUTTON = Button(self.MAIN_WIN, text="Quit", command=self.do_quit)
        self.QUIT_BUTTON.grid(row=1, column=0, padx=5, pady=5)
        self.RESET_BUTTON = Button(self.MAIN_WIN, text="Reset", command=self.reset_game)
        self.RESET_BUTTON.grid(row=2, column=0, padx=5, pady=5)

        self.GAME_CANVAS = Canvas(self.MAIN_WIN, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT, bg="powderblue")
        self.GAME_CANVAS.grid(row=1, column=1, padx=20, pady=20, rowspan=2)
        self.GAME_CANVAS.bind_all("<Key>", self.move_toward)

        self.ACTION_LABEL = Label(self.MAIN_WIN, text="action", font="Arial 16", justify=CENTER, bd=3)
        self.ACTION_LABEL.grid(row=3, column=1, padx=10, pady=10)

        self.tiles = {}
        self.piranhas = False
        self.action = ""

        self.game_over = False

        self.draw_tiles()

    def go(self):
        self.MAIN_WIN.mainloop()

    def draw_tiles(self):
        """Draws the maze walls, the goal, and the ball at its starting location."""
        # self.my_circle = self.tile_canvas.create_rectangle(40, 40, 76, 76, fill="blue")

        for x in range(self.BOARD_LENGTH):
            start_tile_x = x * self.TILE_SIZE + self.START_BOARD_X
            for y in range(self.BOARD_LENGTH):
                start_tile_y = y * self.TILE_SIZE + self.START_BOARD_Y
                tile_colour = self.COLOURS[random.randint(0, len(self.COLOURS) - 1)]
                tile = self.GAME_CANVAS.create_rectangle(start_tile_x,
                                                         start_tile_y,
                                                         start_tile_x + self.TILE_SIZE,
                                                         start_tile_y + self.TILE_SIZE,
                                                         fill=tile_colour,
                                                         outline=tile_colour)
                self.tiles[tile] = tile_colour

        self.my_circle = self.GAME_CANVAS.create_oval(self.START_BOARD_X-self.TILE_SIZE+5,
                                                      205, self.START_BOARD_X-5,
                                                      255, fill="white")
        self.goal = self.GAME_CANVAS.create_text(self.CANVAS_WIDTH-50, self.CANVAS_HEIGHT/2, text="GOAL", fill="black")

    def move_toward(self, event):
        """Callback for clicking on the canvas widget. It looks to see if there are
        circles drawn close to the place where the user clicked. If so, then it removes
        those circles. If not, then it draws a circle centered where the user clicked."""

        # if self.game_over:  # If game is over, don't let it keep playing
        #     return

        (x1, y1, x2, y2) = self.GAME_CANVAS.coords(self.my_circle)

        dx = 0      # delta x
        dy = 0

        if event.keysym == "Right" and x2 <= self.CANVAS_WIDTH-100:
            dx = 2
        elif event.keysym == "Left" and x1 >= 100:
            dx = -2
        elif event.keysym == "Up" and y1 >= 50:
            dy = -2
        elif event.keysym == "Down" and y2 <= self.CANVAS_HEIGHT-50:
            dy = 2

        for d in range(30):
            self.GAME_CANVAS.move(self.my_circle, dx, dy)
            self.MAIN_WIN.update()
            time.sleep(.008)

        self.check_action()

        if self.action == "slide. lemon-scented":
            for d in range(30):
                self.GAME_CANVAS.move(self.my_circle, dx, dy)
                self.MAIN_WIN.update()
                time.sleep(.004)
            self.check_action()

        # account for case of going out of bounds with purple
        if self.action in self.SEND_BACK_COMMANDS:
            if self.action == "stop":
                self.GAME_CANVAS.move(self.my_circle, -dx*30, -dy*30)
            else:
                for d in range(30):
                    self.GAME_CANVAS.move(self.my_circle, -dx, -dy)
                    self.MAIN_WIN.update()
                    time.sleep(.004)

        self.action = ""

    def check_action(self):
        """Checks to see if the player's circle is touching a tile, and which color tile that is"""

        (x1, y1, x2, y2) = self.GAME_CANVAS.coords(self.my_circle)
        on_items = self.GAME_CANVAS.find_overlapping(x1, y1, x2, y2)
        # If more than one overlaps, then the square is touching a wall or the goal
        if len(on_items) > 1:
            for item in on_items:
                if item in self.tiles:
                    self.do_action(self.tiles[item], x1-self.TILE_SIZE-7, y1-self.TILE_SIZE-7,
                                   x2+self.TILE_SIZE+7, y2+self.TILE_SIZE+7)
                    self.ACTION_LABEL["text"] = self.action
                    # self.game_canvas.itemconfigure(self.my_circle, fill=self.tiles[item])
                elif item == self.goal:
                    self.game_over = "win"
                    break
        # Display win/loss message if game is over
        if self.game_over == 'win':
            self.GAME_CANVAS.create_oval(50, 50, 350, 350, fill="yellow")
            self.GAME_CANVAS.create_text(200, 200, text="You've won!")

    def do_action(self, current_colour, x1, y1, x2, y2):
        """Takes in color. Checks colours of surrounding blocks and gives resulting action"""
        zap = False
        if current_colour == "red":
            self.action = "stop"
        elif current_colour == "pink":
            self.action = "pass"
        elif current_colour == "yellow":
            self.GAME_CANVAS.itemconfigure(self.my_circle, fill=current_colour)
            self.MAIN_WIN.update()
            time.sleep(.5)
            self.GAME_CANVAS.itemconfigure(self.my_circle, fill="white")
            self.action = "electrocution"
        elif current_colour == "green":
            self.action = "monster"
        elif current_colour == "orange":
            self.piranhas = True
            self.action = "orange-scented"
        elif current_colour == "blue":
            # check for yellow surrounding tile
            string = ""
            surrounding_tiles = self.GAME_CANVAS.find_enclosed(x1, y1, x2, y2)
            surrounding_tiles_length = len(surrounding_tiles)
            touching_tiles = []
            # maybe change to find_closest? figure out what to do if at edge of board
            if surrounding_tiles_length == 8:
                for i in range(1, len(surrounding_tiles), 2):
                    touching_tiles.append(surrounding_tiles[i])
            for tile in touching_tiles:
                if tile in self.tiles:
                    string = string + self.tiles[tile]
                    if self.tiles[tile] == "yellow":
                        zap = True
            if self.piranhas:
                self.GAME_CANVAS.itemconfigure(self.my_circle, fill=current_colour)
                self.MAIN_WIN.update()
                time.sleep(.5)
                self.GAME_CANVAS.itemconfigure(self.my_circle, fill="white")
                self.action = "piranhas"
            elif zap:
                self.GAME_CANVAS.itemconfigure(self.my_circle, fill="yellow")
                self.MAIN_WIN.update()
                time.sleep(.5)
                self.GAME_CANVAS.itemconfigure(self.my_circle, fill="white")
            else:
                self.action = "swim"
        elif current_colour == "purple":
            self.piranhas = False
            self.action = "slide. lemon-scented"

    def reset_game(self):
        """Resets the game to play again."""
        self.game_over = False
        self.GAME_CANVAS.delete("all")
        self.draw_tiles()

    def do_quit(self):
        """Callback function for the Quit button, closes the main window and ends the
        event loop."""

        self.MAIN_WIN.destroy()


# ========================================================================
def main():
    wall = WallGUI()
    wall.go()


if __name__ == '__main__':
    main()
