"""
Battleship Project
Name:
Roll No:
"""

import battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["no of rows"]=10
    data["no of cols"]=10
    data["boardsize"]=500
    data["cell size"]=50
    data["ships on computer boards"]=5
    data["ships on user boards"]=5
    data["computer board"]=emptyGrid(data["no of rows"],data["no of cols"])
    data["user board"]=emptyGrid(data["no of rows"],data["no of cols"])
    data["computer board"]=addShips(data["computer board"],data["ships on computer boards"])
    data["temporary ship"]=[]
    data["userAddedship"]=0
    data["winner"]=None
    data["max turns"]=50
    data["current turns"]=0
    return 


'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data,userCanvas,data["user board"],True)
    drawGrid(data,compCanvas,data["computer board"],False)
    drawShip(data,userCanvas,data["temporary ship"])
    drawGameOver(data,userCanvas)
    return


'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.keysym=="Return":
        makeModel(data)
    return


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    cell=getClickedCell(data,event)
    if board=="user":
        clickUserBoard(data,cell[0],cell[1])
    elif board=="comp":
        runGameTurn(data,cell[0],cell[1])
    return

#### WEEK 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''

def emptyGrid(rows, cols):
    grid=[]
    for i in range(rows):
        innerlist=[]
        for j in range(cols):
            innerlist.append(EMPTY_UNCLICKED)
        grid.append(innerlist)
    return grid


'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    rowcenter=random.randint(1,8)
    colcenter=random.randint(1,8)
    edge=random.randint(0,1)
    ship=[[]]
    if edge==0:
        ship=[[rowcenter-1,colcenter],[rowcenter,colcenter],[rowcenter+1,colcenter]] #vertical
    else:
        ship=[[rowcenter,colcenter-1],[rowcenter,colcenter],[rowcenter,colcenter+1]] #horizontal
    return ship


'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    count=0
    for i in ship:
        if grid[i[0]][i[1]]==EMPTY_UNCLICKED:
            count=count+1
            if count==len(ship):
                return True
        else:
            return False



'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    count=0
    while count<numShips:
        ship=createShip()
        if checkShip(grid, ship)==True:
            for i in ship:
                grid[i[0]][i[1]]=SHIP_UNCLICKED
            count=count+1
    return grid

   




'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    for row in range(data["no of rows"]):
        for col in range(data["no of cols"]):
            if grid[row][col]==SHIP_UNCLICKED:
                canvas.create_rectangle(data["cell size"]*col,data["cell size"]*row,data["cell size"]*(col+1),data["cell size"]*(row+1),fill="yellow")
            elif grid[row][col]==EMPTY_UNCLICKED:
                canvas.create_rectangle(data["cell size"]*col,data["cell size"]*row,data["cell size"]*(col+1),data["cell size"]*(row+1),fill="blue")
            elif grid[row][col]==SHIP_CLICKED:
                canvas.create_rectangle(data["cell size"]*col,data["cell size"]*row,data["cell size"]*(col+1),data["cell size"]*(row+1),fill="red")
            elif grid[row][col]==EMPTY_CLICKED:
                canvas.create_rectangle(data["cell size"]*col,data["cell size"]*row,data["cell size"]*(col+1),data["cell size"]*(row+1),fill="white")
            if (grid[row][col]==SHIP_UNCLICKED) and (showShips==False):
                canvas.create_rectangle(data["cell size"]*col,data["cell size"]*row,data["cell size"]*(col+1),data["cell size"]*(row+1),fill="blue")
    return data


### WEEK 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    if ship[0][1]== ship[1][1] == ship[2][1]:  
        ship.sort()
        for i in ship:
            if ship[0][0]+1==ship[1][0]==ship[2][0]-1:
                return True 
    return False


'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    if ship[0][0]== ship[1][0] == ship[2][0]:  
        ship.sort()
        for i in ship:
            if ship[0][1]+1==ship[1][1]==ship[2][1]-1:
                return True  
    return False

    


'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    x_coordinate=int(event.x/data["cell size"])
    y_coordinate=int(event.y/data["cell size"])
    return[y_coordinate,x_coordinate]


    


'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    for i in range(len(ship)):
        canvas.create_rectangle(data["cell size"]*(ship[i][1]), data["cell size"]*(ship[i][0]), data["cell size"]*(ship[i][1]+1), data["cell size"]*(ship[i][0]+1), fill="white")
    return
    


'''dddd
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if len(ship)==3:
        if checkShip(grid,ship) and (isVertical(ship) or (isHorizontal(ship))):
            return True
    return False

    


'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    if shipIsValid(data["user board"],data["temporary ship"]):
        for ship in data["temporary ship"]:
            data["user board"][ship[0]][ship[1]]=SHIP_UNCLICKED
        data["userAddedship"]=data["userAddedship"]+1
    else:
        print("Ship is not valid")
    data["temporary ship"]=[]
    return


'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if data["userAddedship"]==5:
        print("You can start the game")
        return
    if [row,col] not in data["temporary ship"]:
        data["temporary ship"].append([row,col])
        if len(data["temporary ship"])==3:
            placeShip(data)
    return


### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board==data["computer board"] or data["user board"]:
        if board[row][col]==SHIP_UNCLICKED:
            board[row][col]=SHIP_CLICKED
        elif board[row][col]==EMPTY_UNCLICKED:
            board[row][col]=EMPTY_CLICKED
    if isGameOver(board):
        data["winner"]=player
    return



'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    if (data["computer board"][row][col]==SHIP_CLICKED) or (data["computer board"][row][col]==EMPTY_CLICKED):
        return
    else:
        updateBoard(data,data["computer board"],row,col,"user")
    click=getComputerGuess(data["user board"])
    updateBoard(data,data["user board"],click[0],click[1],"comp")
    data["current turns"]=data["current turns"]+1
    if data["current turns"]==data["max turns"]:
        data["winner"]="draw"
        

    


'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    row=random.randint(0,9)
    col=random.randint(0,9)
    while board[row][col]==EMPTY_CLICKED or board[row][col]==SHIP_CLICKED:
        row=random.randint(0,9)
        col=random.randint(0,9)
    if board[row][col]==EMPTY_UNCLICKED or board[row][col]==SHIP_UNCLICKED:
        return [row,col]


'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col]==SHIP_UNCLICKED:
                return False
    return True
    


'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''#Helvetica
def drawGameOver(data, canvas):
    if data["winner"]=="user":
        canvas.create_text(200, 70, text="Congrats! You won!", fill="black", font=("Helvetica 20 bold"))
        canvas.create_text(350, 100, text="PRESS ENTER TO PLAY AGAIN!", fill="black", font=("Helvetica 15 bold"))
    if data["winner"]=="comp":
        canvas.create_text(200, 70, text="Try Again! You Lost!", fill="black", font=("Helvetica 20 bold"))
        canvas.create_text(350,100, text="PRESS ENTER TO PLAY AGAIN!", fill="black", font=("Helvetica 15 bold"))
    if data["winner"]=="draw":
        canvas.create_text(200, 70, text="It's a DRAW! Out of moves!", fill="black", font=("Helvetica 20 bold"))
        canvas.create_text(350, 100, text="PRESS ENTER TO PLAY AGAIN!", fill="black", font=("Helvetica 15 bold"))
    return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###ss

# This code runs the test cases to check your work
if __name__ == "__main__":
#changes
    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)
    #test.testDrawShip()
    #test.testUpdateBoard()
    # test.testGetComputerGuess()\
    #test.testIsGameOver()