""" ======================================================================
File: hw6Code.py
Author: put your name here

"""

# -----------------
# Put import statements here

import random
from tkinter import *
import time


class WallGUI:
    """Draws a GUI window with a title label, a quit button, and a canvas with a green
    backdrop. The canvas responds to mouse clicks with the moveToward callback function.
    The Quit button responds to clicks with the doQuit callback function.
    This program allows the user to move a rectangle around"""

    def __init__(self):
        self.gameOver = False

        self.mainWin2 = Tk()
        self.mainWin2.title("Watch the Walls!")

        self.titleLabel = Label(self.mainWin2, text="Watch the Walls!",
                                font="Arial 20 bold", relief=GROOVE,
                                justify=CENTER, bd=5)
        self.titleLabel.grid(row=0, column=1, padx=10, pady=10)

        self.quitButton = Button(self.mainWin2, text="Quit", command=self.doQuit)
        self.quitButton.grid(row=1, column=0, padx=5, pady=5)
        self.resetButton = Button(self.mainWin2, text="ResetGame", command=self.resetGame)
        self.resetButton.grid(row=2, column=0, padx=5, pady=5)

        self.wallCanvas = Canvas(self.mainWin2, width=400, height=400, bg="light green")
        self.wallCanvas.grid(row=1, column=1, padx=20, pady=20, rowspan=2)
        self.wallCanvas.bind("<Button-1>", self.moveToward)
        self.drawMaze()


    def go(self):
        self.mainWin2.mainloop()


    def drawMaze(self):
        """Draws the maze walls, the goal, and the ball at its starting location."""
        self.mySquare = self.wallCanvas.create_rectangle(40, 40, 76, 76, fill="blue")
        self.goal = self.wallCanvas.create_rectangle(230, 250, 280, 300, fill="green", outline="green")
        text = self.wallCanvas.create_text(255, 275, text="GOAL", fill="white")
        wallBounds = [[0, 0, 10, 410], [0, 0, 410, 10], [0, 395, 410, 410], [395, 0, 405, 410],
                      [0, 130, 70, 140], [60, 200, 135, 210], [0, 260, 35, 270], [75, 320, 135, 330],
                      [125, 0, 135, 330], [200, 310, 350, 320], [200, 160, 340, 170], [200, 160, 210, 320],
                      [330, 85, 340, 160], [225, 0, 235, 95]]
        self.wallIDList = []
        for (ulx, uly, lrx, lry) in wallBounds:
            wall = self.wallCanvas.create_rectangle(ulx, uly, lrx, lry, fill="red", outline="red")
            self.wallIDList.append(wall)

        print(self.wallIDList)


    def moveToward(self, event):
        """Callback for clicking on the canvas widget. It looks to see if there are
        circles drawn close to the place where the user clicked. If so, then it removes
        those circles. If not, then it draws a circle centered where the user clicked."""

        if self.gameOver:  # If game is over, don't let it keep playing
            return
        ex = event.x
        ey = event.y
        # Compute center point of player's square
        (x1, y1, x2, y2) = self.wallCanvas.coords(self.mySquare)
        cx= (x1 + x2) / 2
        cy = (y1 + y2) / 2
        # If mouse click is further in x direction and in y direction, move in x direction
        if abs(ex - cx) > abs(ey - cy):
            deltaY = 0
            diff = ex - cx
            if diff >= 0:
                deltaX = 10
            else:
                deltaX = -10
        else:       # Otherwise, move in y direction
            deltaX = 0
            diff = ey - cy
            if diff >= 0:
                deltaY = 10
            else:
                deltaY = -10

        # Move the square
        self.wallCanvas.move(self.mySquare, deltaX, deltaY)

        # Check if game is over
        self.checkForEndOfGame()


    def checkForEndOfGame(self):
        """Checks to see if the player's square is either touching a wall or touching the goal, and if so it
        marks the game as over and displays a game-over message. Note that find_overlapping always includes the
        square itself!"""
        # Find list of items on canvas that overlap with region of square
        (x1, y1, x2, y2) = self.wallCanvas.coords(self.mySquare)
        onItems = self.wallCanvas.find_overlapping(x1, y1, x2, y2)
        # If more than one overlaps, then the square is touching a wall or the goal
        if len(onItems) > 1:
            for item in onItems:
                if item in self.wallIDList:
                    self.gameOver = "loss"
                    self.wallCanvas.addtag_withtag()
                    break
                elif item == self.goal:
                    self.gameOver = "win"
                    break
        # Display win/loss message if game is over
        if self.gameOver == 'win':
            self.wallCanvas.create_oval(50, 50, 350, 350, fill="yellow")
            self.wallCanvas.create_text(200, 200, text="You've won!")
        elif self.gameOver == 'loss':
            self.wallCanvas.create_oval(50, 50, 350, 350, fill="saddle brown")
            self.wallCanvas.create_text(200, 200, text="You've lost!")



    def resetGame(self):
        """Resets the game to play again."""
        self.gameOver = False
        self.wallCanvas.delete("all")
        self.drawMaze()

    def doQuit(self):
        """Callback function for the Quit button, closes the main window and ends the
        event loop."""

        self.mainWin2.destroy()


def main():
    wall = WallGUI()
    wall.go()


if __name__ == '__main__':
    main()


