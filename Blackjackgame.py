import random


suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True


#class definitions:

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank)) #this makes Card objects using the suits in the suits list and the ranks in the rank list and adds to the deck list.

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n" + card.__str__()
        return "The deck has: " + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        one_card = self.deck.pop()
        return one_card


class Hand:
    def __init__(self):
        self.cards = []  # starting with empty list
        self.value = 0   # starting with zero
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self,card):
        self.cards.append(card)
        self.value += values.get(card.rank)
        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet
		

# function definitinos:

def take_bet(chips):

    while True:
        try:
            chips.bet = int(input("How many of your chips would you like to bet in the upcoming game? Please enter a value up to {}: ".format(chips.total)))
        except ValueError:
            print("You have to enter a numerical value. Please try again.")
        else:
            if chips.bet > chips.total:
                print("You cannot bet more chips than you brought with you! Try again with an amount smaller than or equal to {}.".format(chips.total))
            else:
                break


def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop

    while True:

        x = input("Would you like to be hit with another card or stand? Enter 'h' or 's': ")
        if x.lower() == 'h':
            hit(deck, hand)
        elif x.lower() == 's':
            playing = False
        else:
            print("Try again!")
        break


def show_some(player,dealer):

    print("\nThe casino's hand shows only the second card: {}".format(dealer.cards[1]))
    print("\nYour cards are as follows:")
    for card in player.cards:
        print(card)

def show_all(player,dealer):

    print("\nThe Casino has the following hand:")
    for card in dealer.cards:
        print(card)
    print("\nThese are your cards:")
    for card in player.cards:
        print(card)


def player_busts(chips):
    chips.lose_bet()
    print("You are BUST!")

def player_wins(chips):
    chips.win_bet()
    print("You won!")

def dealer_busts(chips):
    chips.win_bet()
    chips.win_bet()
    print("The casino has gone BUST! You win double your bet!")

def dealer_wins(chips):
    chips.lose_bet()
    print("The casino won this game.")

def push():
    print("It's a tie. Well played.")


# gameplay:

print("Welcome to the casino! Would you be partial to a game of Blackjack?")

player_chips = Chips() # Set up the Player's chips outside the loop so game keeps track of how much is won/lost:


while True:

    # Create & shuffle the deck, deal two cards to each player
    my_deck = Deck()
    my_deck.shuffle()

    casino_hand = Hand()
    hit(my_deck, casino_hand)
    hit(my_deck, casino_hand)

    player_hand = Hand()
    hit(my_deck, player_hand)
    hit(my_deck, player_hand)

    

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, casino_hand)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand (geta a card, update card count and adjust for aces)
        hit_or_stand(my_deck, player_hand)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, casino_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:

        while casino_hand.value < 17:
            hit(my_deck, casino_hand)

        # Show all cards
        show_all(player_hand, casino_hand)

        # Run different winning scenarios
        if casino_hand.value > 21:
            dealer_busts(player_chips)

        elif casino_hand.value > player_hand.value:
            dealer_wins(player_chips)

        elif casino_hand.value < player_hand.value:
            player_wins(player_chips)

        else:
            push()

    # Inform Player of their chips total
    print("You currently have {} chips in your precious possession.".format(player_chips.total))

    # Ask to play again
    new_game = input("Would you like to play again? Enter 'y' or 'n': ")
    if new_game[0].lower() == 'y':
        playing = True
    else:
        print("Thanks for playing! See you soon!")
        break
