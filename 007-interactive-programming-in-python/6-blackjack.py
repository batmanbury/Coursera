# Runs on CodeSkulptor.org
# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# global variables
in_play = False
outcome = ""
score = 0
dealer_wins = 0
player_wins = 0

# globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        

class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        hand_str = ''
        for c in self.cards:
            hand_str += str(c) + ' '
        return 'Hand contains' + ' ' + hand_str

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        aces = False
        for c in self.cards:
            value += VALUES[c.get_rank()]
            if 'A' in c.get_rank():
                aces = True
        if aces == True and value <= 11:
            value += 10
        return value
    
    def draw(self, canvas, pos):
        p = list(pos)
        self.cards[0].draw(canvas, p)         # draw the first card fully visible
        for i in range(1, len(self.cards)):
            self.cards[i].draw(canvas, [p[0] + CARD_SIZE[0], p[1]])
            p[0] += CARD_SIZE[0] / 5          # overlap each new card
 
        
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()	# deal a card object from the deck
    
    def __str__(self):
        return ' '.join(self.deck)	# return a string representing the deck


def deal():
    global outcome, score, in_play, dealerHand, playerHand, newDeck
    
    if outcome == 'Hit or Stand?':
        score -= 1
    
    newDeck = Deck()
    newDeck.shuffle()
    playerHand = Hand()
    dealerHand = Hand()
    
    # deal the cards
    playerHand.add_card(newDeck.deal_card())
    dealerHand.add_card(newDeck.deal_card())
    playerHand.add_card(newDeck.deal_card())
    dealerHand.add_card(newDeck.deal_card())
    
    outcome = 'Hit or Stand?'    
    in_play = True

    
def hit():
    global in_play, outcome, score, dealer_wins, playerHand
    
    if in_play == True:
        playerHand.add_card(newDeck.deal_card())
        if playerHand.get_value() > 21:
            outcome = 'You have busted'
            score -= 1
            dealer_wins += 1
            in_play = False
    else:
        outcome = 'New deal?'

        
def stand():
    global in_play, outcome, score, dealer_wins, player_wins, dealerHand
    if in_play == True:
        while dealerHand.get_value() < 17:
            dealerHand.add_card(newDeck.deal_card())
        if dealerHand.get_value() > 21:
            outcome = 'Dealer has busted'
            score += 1
            player_wins += 1
        elif dealerHand.get_value() >= playerHand.get_value():
            outcome = 'Dealer wins'
            score -= 1
            dealer_wins += 1
        else:
            outcome = 'Player wins!'
            score += 1
            player_wins += 1
        in_play = False
    else:
        outcome = 'New deal?'


def draw(canvas):
    
    # title, arc, outcome message, score
    canvas.draw_text('Blackjack', [200, 40], 50, 'Black', 'serif')
    canvas.draw_text('DEALER WINS ALL TIES', [175, 75], 22, 'Black', 'sans-serif')
    canvas.draw_circle([300, -300], 400, 5, 'Maroon')
    canvas.draw_circle([300, -300], 405, 5, 'Black')
    canvas.draw_circle([300, -300], 410, 5, 'Maroon')
    canvas.draw_text(outcome, [100, 310], 35, 'Yellow', 'sans-serif')
    canvas.draw_text('Score: ' + str(score), [100, 520], 40, 'White', 'sans-serif')
    
    # dealer hand value, wins, cards, hole card
    canvas.draw_text('Dealer Wins: ' + str(dealer_wins), [370, 170], 30, 'Yellow', 'sans-serif')
    dealerHand.draw(canvas, [100, 150])
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [CARD_CENTER[0]+100, CARD_CENTER[1]+150], CARD_BACK_SIZE)
    if in_play == False:
        canvas.draw_text('Dealer has ' + str(dealerHand.get_value()), [100, 142], 20, 'Black', 'sans-serif')
        
    # player hand value, wins, cards
    canvas.draw_text('Player has ' + str(playerHand.get_value()), [100, 472], 20, 'Black', 'sans-serif')
    canvas.draw_text('Player Wins: ' + str(player_wins), [370, 370], 30, 'Yellow', 'sans-serif')
    playerHand.draw(canvas, [100, 350])
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 550)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
