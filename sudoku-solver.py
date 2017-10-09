import numpy as np

from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font

#Create puzzle GUI layout
root = tk.Tk()
root.title("Sudoku Solver")

mainframe = ttk.Frame(root, padding="15")
mainframe.grid(column=0, row=0, stick=(N, W, E, S))

mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="Sudoku Solver", anchor="center").grid(column=1, columnspan=10, row=0, sticky=(W,E))

#Create a grid of Entry widgets and declare each Entry as a Tk variable - StringVar()
position ={}
pos = 1
for x in range(0,9):
    for y in range(0,9):
        position[pos] = StringVar()
        ttk.Entry(mainframe, width=2, textvariable=position[pos]).grid(row=x+1, column=y+1, sticky=(W,E))
        pos += 1

#Create board and set sub-grids to be view of the main board
board = np.zeros((9,9), dtype=np.int64)

a = board[0:3, 0:3]
b = board[0:3, 3:6]
c = board[0:3, 6:9]
d = board[3:6, 0:3]
e = board[3:6, 3:6]
f = board[3:6, 6:9]
g = board[6:9, 0:3]
h = board[6:9, 3:6]
i = board[6:9, 6:9]
subGrids = [a,b,c,d,e,f,g,h,i]

#Assign the Entry value to the board elements

def set_puzzle(*args):    
    idx = 1
    for x in range(0,9):
        for y in range(0,9):
            if len(position[idx].get()) == 0:
                board[x,y] = 0
            else:
                value = int(position[idx].get())
                board[x,y] = value
            idx += 1

#Function to find all possible numbers for each sub-grid
def possibleEntry(arr2, arr1=np.arange(1,10)):
    if(len(arr1) == 0): #if comparing array is empty, just return the other array
        return arr2
    else:
        choice = np.setdiff1d(arr1, arr2)
        if(len(choice) > 0): #if not empty join into a single number
            choice = int(''.join(str(i) for i in choice))
            return choice
        else: #if empty, return empty array
            return choice

#Eliminate the numbers in the row and column and assign possible numbers to "empty" elements
def crosshatch(board):
    #set array to add possible numbers to, based on row and column
    pool = np.empty(0, dtype=np.int64)
    
    board_length = board.shape[0]
    for x in range(board_length): #row
        for y in range(board_length): #column
            #if element is longer than 1 digit check its row and column
            if (len(str(board[x,y])) > 1 ): 

                pool = np.append(pool, board[x, :]) #append all the numbers in that element's row
                pool = np.append(pool, board[:, y]) #append all the numbers in that element's column
                pool = pool[ pool < 10] #eliminate any number laster than 9

                current = [int(i) for i in str(board[x,y])] #convert current element into an array of numbers
                np.asarray(current, dtype=np.int64)
            
                #assign the element to a new possibleEntry
                board[x,y] = possibleEntry(pool, current)
            
                #reset the pool for the next element
                pool = np.empty(0, dtype=np.int64)
    
    return board

#Function to check if puzzle is complete
def checkGrid(board):
    board_length = board.shape[0]
    for x in range(board_length): #row
        for y in range(board_length): #column
            if (board[x,y] > 9 or int(board[x,y]) == 0):
                return False
    return True

#Solve function - once solved assign numbers of the board elements to each Entry widget to dsiplay on GUI
def solve(*args): 
    set_puzzle()
    while checkGrid(board) == False:
        for i in subGrids:
            i[i == 0] = possibleEntry(i)
            crosshatch(board)
        
    idx = 1
    for x in range(0,9):
        for y in range(0,9):
            position[idx].set(board[x,y])
            idx += 1

#Add bottuns on the bottom and assign the functions
ttk.Button(mainframe, text="Solve", command=solve).grid(column=1, columnspan=5, row=12, sticky=(W, E))
ttk.Button(mainframe, text="Clear").grid(column=6, columnspan=5, row=12, sticky=(W, E))

root.mainloop()








