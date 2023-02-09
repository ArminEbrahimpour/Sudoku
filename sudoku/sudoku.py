import pygame
#import requests
from sys import exit
import copy

# set the variables
board = []
solution = []
user_board  = []
WIDTH = 550
background_color = (9, 27, 56)

def delete_pos(row, col):
    # we dont want to delete any part of the line of the main board 
    # so this scope of code will mangage the x and y of our fill method to 
    # delete the number not any part of the main board
    if col == 1 or col == 4 or col == 7:
        x_1 = 50*col + 3

    elif col == 3 or col == 2 or col == 5 or col == 6 or col == 8 or col == 9:
        x_1 = 50*col + 2
        
    # managing the y of the fill method 
    if row == 1 or row == 4 or row == 7:
        y_1 = 50*row + 3

    elif row == 3 or row == 2 or row == 5 or row == 6 or row == 8 or row == 9:
        y_1 = 50*row + 3
    return x_1,y_1

# this will compare every element of  user_board and solution list and change the correct element's color to green 
def check_board(screen):
    for i in range(0, 9):
        for j in range(0, 9):
            if user_board[i][j] == solution[i][j]:
                # the below if checks if it is not numbers set by computer at first (keep white numbers)
                if board[i][j] == 0:
                    # converting i and j to x and y for calling our functions
                    # row = i + 1 and col = j + 1
                    row = i + 1
                    col = j + 1
                    x_1,y_1 = delete_pos(row, col)

                    # Deleting the white number 
                    screen.fill(background_color,(x_1, y_1, 48,48))

                    # render the number in green color
                    Font = pygame.font.SysFont("Comic Sans MS", 35)
                    value = Font.render(str(user_board[i][j]), True, (28,72,0))

                    screen.blit(value, ((col)*50 + 15, (row)*50 + 15 ))


# will check if the board is full or not
def Game_finished():
    global user_board
    
    game_finished =True
    for i in range(0, 9):
        for j in range(0, 9):
            if user_board[i][j] == 0:
                game_finished = False
    
    return game_finished


# this function return True if the place in board was empty
def is_empty(row, col):
    flag = True

    if board[row-1][col-1] != 0:# the minus 1 is because of list index starts by 0 but row and col start by 1
        flag = False

    return flag

def Row_Col(x, y):
    row =0
    col =0
        # these two for loop will get the row and column of the position that mouse clicked
    for i in range(50, 500, 50):
        if i <= x <= i + 50:
            col = i //50
    
    for j in range(50, 500, 50):
        if j <= y <= j + 50:
            row = j // 50

    return row,col

def delete_number(x, y, screen):
    global user_board
    row =0
    col =0
    #screen.fill(background_color, (x_1,y_1,x_2,y_2))


    # the function set the row and col variable
    row, col = Row_Col(x, y)

    # checks if the block is empty or not
    if is_empty(row, col):

        x_1,y_1 = delete_pos(row, col)
        
        # expand variable
        plus = 48

        screen.fill(background_color, (x_1,y_1,plus,plus))

        # set the deleted number in main board list to 0 
        user_board[row-1][col-1] = 0


# this function will attach on the positon 
def set_at_pos(x, y, screen, num,    color = (192,10,0)):
    global user_board
    col = 0
    row = 0
    # color = (192,10,0)


    # the function set the row and col variable
    row, col = Row_Col(x, y)

    # for line in solution:
    #     print(line)

    if is_empty(row, col):
        Font = pygame.font.SysFont("Comic Sans MS", 35)
        value = Font.render(str(num), True, color)

        screen.blit(value, ((col)*50 + 15, (row)*50 + 15 ))

        # append the number into the main list that represent of the screen board 
        user_board[row-1][col-1] = num

        if Game_finished():
            #print("Finished")
            check_board(screen)


# this scope of code will make the valid pattern board for the game
def puzzleMaker():
    global board
    global solution
    global user_board
    base  = 3
    side  = base*base

    # pattern for a baseline valid solution
    def pattern(r,c): return (base*(r%base)+r//base+c)%side

    # randomize rows, columns and numbers (of valid base pattern)
    from random import sample
    def shuffle(s): return sample(s,len(s)) 
    rBase = range(base) 
    rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
    cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
    nums  = shuffle(range(1,base*base+1))

    # produce board using randomized baseline pattern
    board = [ [nums[pattern(r,c)] for c in cols] for r in rows ] 
    solution = copy.deepcopy(board)

    for line in board: print(line)

    squares = side*side
    empties = squares * 3//4
    for p in sample(range(squares),empties):
        board[p//side][p%side] = 0
    user_board = copy.deepcopy(board)

    numSize = len(str(side))


# making the board of our playground    
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, WIDTH))
    screen.fill(background_color)
    pygame.display.set_caption("Sudoku By RminEBP")
    screen.fill(background_color)
    for i in range(0,10):
        if(i%3 == 0):
            pygame.draw.line(screen, (50,27,56), (50 + 50*i, 50), (50 + 50*i ,500),4)
            pygame.draw.line(screen, (50,27,56), (50, 50 + 50*i), (500, 50 + 50*i),4)
 
        pygame.draw.line(screen, (50,27,56), (50 + 50*i, 50), (50 + 50*i ,500 ), 2 )
        pygame.draw.line(screen, (50,27,56), (50, 50 + 50*i), (500, 50 + 50*i), 2 )
    pygame.display.update()
    # pygame.draw.line(surface, color, start_pos, end_pos)

    puzzleMaker() # now we should implement the board list

    buffer = 5

    Font = pygame.font.SysFont("Comic Sans MS", 35)

    for i in range(0, 9):
        for j in range(0, 9):
            if board[i][j] != 0:
                value = Font.render(str(board[i][j]), True, (192,192,192))
                screen.blit(value, ((j+1)*50 + 15, (i+1.25)*50 ))

    pygame.display.update()

    for line in solution:
        print(line)

    # this variable will hold the number that user selected on keyboard
    num = 0
    while(True):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # left click
                
                if 50<x<500 and 50<y<500:
                    set_at_pos(x, y, screen, num)
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: # right click
                # delete the number
                if 50<x<500 and 50<y<500:
                    delete_number(x, y, screen)
                

            if event.type == pygame.KEYDOWN:
                    #select the number before rendering on screen 
                if event.key == pygame.K_1:
                    num = 1
                elif event.key == pygame.K_2:
                    num = 2
                elif event.key == pygame.K_3:
                    num = 3
                elif event.key == pygame.K_4:
                    num = 4
                elif event.key == pygame.K_5:
                    num = 5
                elif event.key == pygame.K_6:
                    num = 6
                elif event.key == pygame.K_7:
                    num = 7
                elif event.key == pygame.K_8:
                    num = 8
                elif event.key == pygame.K_9:
                    num = 9

            
        x, y = pygame.mouse.get_pos()
        #print(x, y)
        pygame.display.update()

try:  
    main()
except:
    pass    