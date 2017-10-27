
#Sudoku Solver - Using the Crosshatching Method

import numpy as np

from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font


#Tk: Create puzzle GUI
root = Tk()
root.title("Sudoku Solver")

mainframe = ttk.Frame(root, padding="15")
mainframe.grid(column=0, row=0, stick=(N, W, E, S))

mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)


#Tk: Set font style to use throughout 
mainFont = font.Font(family='Helvetica', size=18) #weight='bold'
ttk.Label(mainframe, text="Sudoku Solver", anchor="center", font=mainFont).grid(column=1, columnspan=10, row=0, sticky=(W,E))


#Tk: Set style for the Entry widgets: background color
estyle = ttk.Style()
estyle.element_create("plain.field", "from", "clam")

estyle.layout("EntryStyle.Teal",
                   [('Entry.plain.field', {'children': [(
                       'Entry.background', {'children': [(
                           'Entry.padding', {'children': [(
                               'Entry.textarea', {'sticky': 'nswe'})],
                      'sticky': 'nswe'})], 'sticky': 'nswe'})],
                      'border':'2', 'sticky': 'nswe'})])
estyle.configure("EntryStyle.Teal",
                 background="black", 
                 foreground="black",
                 fieldbackground="#cdf2eb")

estyle.layout("EntryStyle.Rose",
                   [('Entry.plain.field', {'children': [(
                       'Entry.background', {'children': [(
                           'Entry.padding', {'children': [(
                               'Entry.textarea', {'sticky': 'nswe'})],
                      'sticky': 'nswe'})], 'sticky': 'nswe'})],
                      'border':'2', 'sticky': 'nswe'})])
estyle.configure("EntryStyle.Rose",
                 background="black", 
                 foreground="black",
                 fieldbackground="#f9f4f4")


#Tk: Create a grid of Entry widgets and declare each Entry as a Tk variable - StringVar()
#Set background color for the Entry widgets as they are declared
#Most of the logic is to set the background style based on the location of the Entry on the board
position ={}

pos = 1
for x in range(0,9):
    n1 = 1
    n2 = 1
    if (x < 3 or x >= 6):
        for y in range(0,9):
            if (n2 - n1) < 3:
                position[pos] = StringVar()
                ttk.Entry(mainframe, width=2, style="EntryStyle.Rose", font=mainFont, textvariable=position[pos]).grid(row=x+1, column=y+1, 			sticky=(W,E))
            elif (n2 - n1) >= 3 or (n2 -n1) < 6:
                position[pos] = StringVar()
                ttk.Entry(mainframe, width=2, style="EntryStyle.Teal", font=mainFont, textvariable=position[pos]).grid(row=x+1, column=y+1, 			sticky=(W,E))
            if (n2 - n1) == 5:
                n1 = n2 + 1
            n2 += 1
            pos += 1
    if (x >= 3 and x < 6):
        for y in range(0,9):
            if (n2 - n1) < 3:
                position[pos] = StringVar()
                ttk.Entry(mainframe, width=2, style="EntryStyle.Teal", font=mainFont, textvariable=position[pos]).grid(row=x+1, column=y+1, 			sticky=(W,E))
            elif (n2 - n1) >= 3 or (n2 -n1) < 6:
                position[pos] = StringVar()
                ttk.Entry(mainframe, width=2, style="EntryStyle.Rose", font=mainFont, textvariable=position[pos]).grid(row=x+1, column=y+1, 			sticky=(W,E))
            if (n2 - n1) == 5:
                n1 = n2 + 1
            n2 += 1
            pos += 1


#Numpy: Create board and set sub-grids to be view of the main board
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


#Tk: Assign the Entry value to the board elements
#If Entry is empty (len(position[i].get()) == 0) the assign that element to zero 0
#If filled assign board element to that value
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


#Tk: Clear the puzzle board:
#Assign each element of the board to 0
#Assign each Tk Entry variable to empty string ""
def clear_puzzle(*args):
    idx = 1
    for x in range(0,9):
        for y in range(0,9):
            position[idx].set("")
            board[x,y] = 0
            idx += 1


#Numpy: Function to find all possible numbers for each sub-grid
#Using numpy.setdiff1d(array1, array2) - Return the sorted, unique values in array1 that are not in array2 (Order matters)
#Convert array of possible choices into a single number
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


#Numpy: Eliminate the numbers in the row and column and assign possible numbers to "empty" elements
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
            
        


#Numpy: Function to check if puzzle is complete
#Returns False if grid contains zeros or numbers larger than 9
def checkGrid(board):
    board_length = board.shape[0]
    for x in range(board_length): #row
        for y in range(board_length): #column
            if (board[x,y] > 9 or int(board[x,y]) == 0):
                return False
    return True
    


#Tk: Solve function - once solved assign numbers of the board elements to each Entry widget to dsiplay on GUI
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

#Set a sample puzzle:
def sample_puzzle(*args):
    a2 = np.array([1,0,0,7,3,0,0,0,0]).reshape((3,3))
    b2 = np.array([4,8,9,0,0,0,0,0,1]).reshape((3,3))
    c2 = np.array([0,0,6,0,4,0,2,9,5]).reshape((3,3))
    d2 = np.array([0,0,7,5,0,0,0,0,6]).reshape((3,3))
    e2 = np.array([1,2,0,7,0,3,0,9,5]).reshape((3,3))
    f2 = np.array([6,0,0,0,0,8,7,0,0]).reshape((3,3))
    g2 = np.array([9,1,4,0,2,0,8,0,0]).reshape((3,3))
    h2 = np.array([6,0,0,0,0,0,5,1,2]).reshape((3,3))
    i2 = np.array([0,0,0,0,3,7,0,0,4]).reshape((3,3))

    row1 = np.concatenate((a2, b2, c2), axis=1) #axis=1 column wise
    row2 = np.concatenate((d2, e2, f2), axis=1)
    row3 = np.concatenate((g2, h2, i2), axis=1)
    board = np.concatenate((row1, row2, row3), axis=0)

    idx = 1
    for x in range(0,9):
        for y in range(0,9):
            if (board[x,y] == 0):
                position[idx].set("")
            else:
                position[idx].set(board[x,y])
            idx += 1


#Tk: Add bottuns on the bottom and assign the functions
#Using tk Button instead of ttk to use background color (bg)
tk.Button(mainframe, bg='#78e2af', fg='#1b3305', relief='flat', text="Solve", command=solve).grid(column=1, columnspan=3, row=12, sticky=(W, E))
tk.Button(mainframe, bg='#efbac9', fg='#30020f', relief='flat', text="Clear", command=clear_puzzle).grid(column=4, columnspan=3, row=12, sticky=(W, E))
tk.Button(mainframe, bg='#d9e4f4', fg='#30020f', relief='flat', text="Example", command=sample_puzzle).grid(column=7, columnspan=3, row=12, sticky=(W, E))


#Tk: End GUI with Tk mainloop
root.mainloop()

