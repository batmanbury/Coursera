# Mini-project 3: "Stopwatch: The Game"

import simplegui


# define global variables
tenths = 0
attempts = 0
wins = 0
running = False


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    a = t / 600
    b = t / 100 % 6
    c = t / 10 % 10
    d = t % 10
    return str(a) + ':' + str(b) + str(c) + '.' +str(d)


# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global running
    running = True
    timer.start()

def stop():
    global running
    global attempts
    global wins
    if running == True:
        attempts += 1
        if tenths % 10 == 0:
            wins += 1
    running = False
    timer.stop()

def reset():
    global tenths
    global attempts
    global wins
    tenths = 0
    attempts = 0
    wins = 0
    timer.stop()


# define event handler for timer with 0.1 sec interval
def stopwatch():
    global tenths
    tenths += 1
    if tenths > 6000:
        reset()
    
    
# define draw handler
def draw(canvas):
    canvas.draw_text(format(tenths), (65, 85), 30, "White")
    canvas.draw_text((str(wins)+'/'+str(attempts)), (145, 25), 30, "Green")

    
# create frame
f = simplegui.create_frame("Stopwatch: The Game", 200, 150)


# register event handlers
f.add_button("Start", start, 75)
f.add_button("Stop", stop, 75)
f.add_button("Reset", reset, 75)
timer = simplegui.create_timer(100, stopwatch)
f.set_draw_handler(draw)


# start frame
f.start()
