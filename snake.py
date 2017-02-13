# snake7.py

import random
from Tkinter import *

def snakeMousePressed(canvas, event):
    pass

def snakeKeyPressed(canvas, event):
    canvas.data.ignoreNextTimerEvent = True
    # first process keys that work even if the game is over
    if (event.char == "q"):
        gameOver(canvas)
    elif (event.char == "r"):
        snakeInit(canvas)
    elif (event.char == "d"):
        canvas.data.inDebugMode = not canvas.data.inDebugMode
    elif (event.char == "h"):
        snakeLength = canvas.data.snakeBoard[canvas.data.headRow][canvas.data.headCol]
        print snakeLength
        for row in xrange(canvas.data.rows):
            for col in xrange(canvas.data.cols):
                if canvas.data.snakeBoard[row][col]>0:
                    if (snakeLength/2)>0:
                        canvas.data.snakeBoard[row][col]-= (snakeLength/2)
                        if canvas.data.snakeBoard[row][col]<0:
                            canvas.data.snakeBoard[row][col] = 0

    # now process keys that only work if the game is not over
    if (canvas.data.isGameOver == False):
        if (event.keysym == "Up"):
            moveSnake(canvas,-1, 0)
        elif (event.keysym == "Down"):
            moveSnake(canvas,+1, 0)
        elif (event.keysym == "Left"):
            moveSnake(canvas,0,-1)
        elif (event.keysym == "Right"):
            moveSnake(canvas,0,+1)
    snakeRedrawAll(canvas)

def moveSnake(canvas, drow, dcol):
    # move the snake one step forward in the given direction.
    canvas.data.snakeDrow = drow # store direction for next timer event
    canvas.data.snakeDcol = dcol
    snakeBoard = canvas.data.snakeBoard
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    headRow = canvas.data.headRow
    headCol = canvas.data.headCol
    newHeadRow = headRow + drow
    newHeadCol = headCol + dcol
    if ((newHeadRow < 0) or (newHeadRow >= rows) or
        (newHeadCol < 0) or (newHeadCol >= cols)):
        # snake ran off the board
        gameOver(canvas)
    elif (snakeBoard[newHeadRow][newHeadCol] > 0):
        # snake ran into itself
        gameOver(canvas)
    elif (snakeBoard[newHeadRow][newHeadCol] < 0):
        # food eaten
        snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol];
        canvas.data.headRow = newHeadRow
        canvas.data.headCol = newHeadCol
        placeFood(canvas)
    else:
        # normal move forward (not eating food)
        snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol];
        canvas.data.headRow = newHeadRow
        canvas.data.headCol = newHeadCol
        removeTail(canvas)

def removeTail(canvas):
    # find every snake cell and subtract 1 from it
    # the old tail (which was 1) will become 0, so will not be part of the snake
    snakeBoard = canvas.data.snakeBoard
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    for row in range(rows):
        for col in range(cols):
            if (snakeBoard[row][col] > 0):
                snakeBoard[row][col] -= 1

def gameOver(canvas):
    canvas.data.isGameOver = True

def snakeTimerFired(canvas):
    if (canvas.data.isGameOver == False):
        # only process snakeTimerFired if game is not over
        drow = canvas.data.snakeDrow
        dcol = canvas.data.snakeDcol
        if canvas.data.ignoreNextTimerEvent == False:
            moveSnake(canvas,drow, dcol)
        canvas.data.ignoreNextTimerEvent = False
        snakeRedrawAll(canvas)
    # whether or not game is over, call next snakeTimerFired
    # (or we'll never call snakeTimerFired again)
    delay = 150 # milliseconds
    def snakeReTimer():
        snakeTimerFired(canvas)
    canvas.after(delay, snakeReTimer) # pause, then call snakeTimerFired again

def snakeRedrawAll(canvas):
    canvas.delete(ALL)
    drawSnakeBoard(canvas)
    if (canvas.data.isGameOver == True):
        cx = canvas.data.canvasWidth/2
        cy = canvas.data.canvasHeight/2
        canvas.create_text(cx, cy, text="Game Over!", font=("Helvetica", 32, "bold"))

def drawSnakeBoard(canvas):
    snakeBoard = canvas.data.snakeBoard
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    for row in range(rows):
        for col in range(cols):
            drawSnakeCell(canvas, row, col)

def drawSnakeCell(canvas, row, col):
    snakeBoard = canvas.data.snakeBoard
    margin = canvas.data.margin
    cellSize = canvas.data.cellSize
    left = margin + col * cellSize
    right = left + cellSize
    top = margin + row * cellSize
    bottom = top + cellSize
    canvas.create_rectangle(left, top, right, bottom, fill="white")
    if (snakeBoard[row][col] > 0):
        # draw part of the snake body
        canvas.create_oval(left, top, right, bottom, fill="blue")
    elif (snakeBoard[row][col] < 0):
        # draw food
        canvas.create_oval(left, top, right, bottom, fill="green")
    # for debugging, draw the number in the cell
    if (canvas.data.inDebugMode == True):
        canvas.create_text(left+cellSize/2,top+cellSize/2,
                           text=str(snakeBoard[row][col]),font=("Helvatica", 14, "bold"))

def loadSnakeBoard(canvas):
    canvas.data.ignoreNextTimerEvent = False
    rows = canvas.data.rows
    cols = canvas.data.cols
    snakeBoard = [ ]
    for row in range(rows): snakeBoard += [[0] * cols]
    snakeBoard[rows/2][cols/2] = 1
    canvas.data.snakeBoard = snakeBoard
    findSnakeHead(canvas)
    placeFood(canvas)

def placeFood(canvas):
    # place food (-1) in a random location on the snakeBoard, but
    # keep picking random locations until we find one that is not
    # part of the snake
    snakeBoard = canvas.data.snakeBoard
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    while True:
        row = random.randint(0,rows-1)
        col = random.randint(0,cols-1)
        if (snakeBoard[row][col] == 0):
            break
    snakeBoard[row][col] = -1

def findSnakeHead(canvas):
    # find where snakeBoard[row][col] is largest, and
    # store this location in headRow, headCol
    snakeBoard = canvas.data.snakeBoard
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    headRow = 0
    headCol = 0
    for row in range(rows):
        for col in range(cols):
            if (snakeBoard[row][col] > snakeBoard[headRow][headCol]):
                headRow = row
                headCol = col
    canvas.data.headRow = headRow
    canvas.data.headCol = headCol

def printInstructions():
    print "Snake!"
    print "Use the arrow keys to move the snake."
    print "Eat food to grow."
    print "Stay on the board!"
    print "And don't crash into yourself!"
    print "Press 'd' for debug mode."
    print "Press 'r' to restart."

def snakeInit(canvas):
    printInstructions()
    loadSnakeBoard(canvas)
    canvas.data.inDebugMode = False
    canvas.data.isGameOver = False
    canvas.data.snakeDrow = 0
    canvas.data.snakeDcol = -1 # start moving left
    snakeRedrawAll(canvas)

def snakeRun(rows, cols):
    # create the root and the canvas
    root = Tk()
    margin = 5
    cellSize = 30
    canvasWidth = 2*margin + cols*cellSize
    canvasHeight = 2*margin + rows*cellSize
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call snakeInit
    class Struct: pass
    canvas.data = Struct()
    canvas.data.margin = margin
    canvas.data.cellSize = cellSize
    canvas.data.canvasWidth = canvasWidth
    canvas.data.canvasHeight = canvasHeight
    canvas.data.rows = rows
    canvas.data.cols = cols
    snakeInit(canvas)
    # set up events
    root.bind("<Button-1>", lambda event: snakeMousePressed(canvas, event))
    root.bind("<Key>", lambda event: snakeKeyPressed(canvas, event))
    snakeTimerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window)

snakeRun(8,16)