# Runs on CodeSkulptor.com
# implementation of card game - Memory

import simplegui
import random

deck_half_1 = range(8)
deck_half_2 = range(8)
deck = deck_half_1 + deck_half_2 #build deck size

exposed = range(16)
for c in exposed:                #set all cards to not exposed
    exposed[c] = False

state = 0
card1 = 0
card2 = 0
turns = 0

# helper function to initialize globals
def new_game():
    global exposed, state, turns
    random.shuffle(deck)
    state = 0
    turns = 0
    label.set_text('Turns = '+str(turns))
    exposed = range(16)
    for c in exposed:            #set all cards to not exposed
        exposed[c] = False


# define event handlers
def mouseclick(click):
    global exposed, state, card1, card2, turns

    if state == 0:
        if not exposed[click[0]//50]:
            exposed[click[0]//50] = True
            card1 = click[0]//50
            state = 1
    
    if state == 1:
        if not exposed[click[0]//50]:
            exposed[click[0]//50] = True
            card2 = click[0]//50
            state = 2
            turns += 1
            label.set_text('Turns = '+str(turns))
    
    if state == 2:
        if not exposed[click[0]//50]:
            if deck[card1] != deck[card2]:
                exposed[card1] = False
                exposed[card2] = False
            exposed[click[0]//50] = True
            card1 = click[0]//50
            state = 1
            

# cards are logically 50x100 pixels in size    
def draw(canvas):
    pos = [0, 82]
    for card in range(16):
        if exposed[card] == False:
            canvas.draw_polygon([(pos[0], 0), (pos[0]+50, 0), (pos[0]+50, 100), (pos[0], 100)], 2, 'White', 'Green')
            pos[0] += 50
        else:
            canvas.draw_text(str(deck[card]), pos, 100, "White")
            pos[0] += 50


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
