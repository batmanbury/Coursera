# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import random
import simplegui


# initialize global variables
turns = 7
num_range = 100
secret_number = 0


# helper function to start and restart the game
def new_game():
    global secret_number
    global turns
    
    secret_number = random.randrange(num_range)
    
    if num_range == 100:
        turns = 7
    else:
        turns = 10
    
    print ""
    print "New game. Range is from 0 to " + str(num_range)
    print "Number of remaining guesses is " + str(turns)


# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global num_range
    global turns
    
    num_range = 100
    turns = 7
    
    new_game()
    

def range1000():
    # button that changes range to range [0,1000) and restarts
    global num_range
    global turns
    
    num_range = 1000
    turns = 10
    
    new_game()
    
    
def input_guess(guess):
    # main game logic goes here	
    global secret_number
    global turns
    
    turns -= 1
    
    print ""
    print "Number of remaining guesses is " + str(turns)
    print "You guessed " + str(guess)
    
    if int(guess) == secret_number:
        print "Correct! You win!"
        print "================================"
        new_game()
    elif turns == 0:
        print "Sorry, out of guesses! You lose!"
        print "================================"
        new_game()
    elif int(guess) < secret_number:
        print "Higher..."
    else:
        print "Lower..."


# create frame
f = simplegui.create_frame("Guess the Number", 200, 200)


# register event handlers for control elements
f.add_button("Range is [0, 100)", range100, 200)
f.add_button("Range is [0, 1000)", range1000, 200)
f.add_input("Enter a number", input_guess, 200)


# call new_game and start frame
f.start()
new_game()


# always remember to check your completed program against the grading rubric