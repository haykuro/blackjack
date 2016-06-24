"""Docstring."""
from random import choice as rand_choice
from itertools import repeat as iter_repeat
from re import findall

def gen_suite(suite):
    """Funcdoc."""
    return [n + suite for n in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']]

class Deck(object):
    """Classdoc."""

    def get_cards(self):
        """Funcdoc."""
        return self.cards

    def pull_card(self):
        """Funcdoc."""
        card = rand_choice(self.cards)
        self.cards.remove(card)
        return card

    def __len__(self):
        """Funcdoc."""
        return len(self.get_cards())

    def __repr__(self):
        """Funcdoc."""
        return "Deck(%d)" % (len(self))

    def __init__(self):
        """Funcdoc."""
        self.cards = []
        for suite in list('CDSH'):
            self.cards += gen_suite(suite)

class Player(object):
    """Classdoc."""

    def set_name(self, name):
        """Funcdoc."""
        self.name = name

    def get_name(self):
        """Funcdoc."""
        return self.name

    def get_hand(self):
        """Funcdoc."""
        return self.hand

    def addto_hand(self, card):
        """Funcdoc."""
        if card:
            self.hand += [card]

    def calc_hand(self):
        """Funcdoc."""
        the_sum = 0
        for card in self.get_hand():
            if card[:1] is "A":
                if (the_sum + 11) < 22:
                    val = 11
                else:
                    val = 1
            elif card[:1] in list('JQK'):
                val = 10
            else:
                nums = findall(r"^\d+", card)
                val = int(nums[0])

            the_sum += val
        return the_sum

    def get_wins(self):
        """Funcdoc."""
        return self.wins

    def set_wins(self, num):
        """Funcdoc."""
        self.wins = num

    def __repr__(self):
        """Funcdoc."""
        return '%s: %d [%s]' % (self.get_name(), self.calc_hand(), self.get_hand())

    def __init__(self, name):
        """Funcdoc."""
        self.hand = []
        self.set_name(name)
        self.set_wins(0)

class Game(object):
    """Classdoc."""

    def pull_card(self):
        """Funcdoc."""
        deck = rand_choice(self.decks)
        if deck and len(deck) > 0:
            return deck.pull_card()
        return False

    def set_decks(self, num):
        """Funcdoc."""
        if num < 1:
            return False

        self.decks = [Deck() for _ in iter_repeat(None, num)]

    def get_players(self):
        """Funcdoc."""
        return self.players

    def add_player(self, player):
        """Funcdoc."""
        self.players += [player]

    def deal(self):
        """Funcdoc."""
        for player in self.get_players():
            player.addto_hand(self.pull_card())
            player.addto_hand(self.pull_card())

    def __init__(self, decks=8):
        """Funcdoc."""
        self.decks = []
        self.players = []
        self.set_decks(decks)

def player_line(player, dealer_hand=False, hide_one=False):
    """Funcdoc."""
    hand = player.get_hand()
    hand_val = player.calc_hand()

    if dealer_hand:
        win = False

        if (dealer_hand > 21 and hand_val < 22) or (hand_val < 22 and hand_val > dealer_hand):
            win = True

        if win:
            return '%s: %s [%s]\n\t%s' % (player.get_name(), hand_val, 'WIN!', ', '.join(hand))

    if hide_one:
        hand = hand[:-1]
        return '%s: %s\n\t%s' % (player.get_name(), '??', ', '.join(hand))

    return '%s: %s\n\t%s' % (player.get_name(), hand_val, ', '.join(hand))

def main():
    """Funcdoc."""
    ## Start a new game
    game = Game(decks=8)
    dealer = Player('Dealer')

    ## Add players
    game.add_player(dealer)
    game.add_player(Player('Steve'))
    game.add_player(Player('Johanna'))
    game.add_player(Player('Leon'))

    ## Deal!
    game.deal()

    print player_line(dealer, hide_one=True)

    ## Play each hand.
    for player in game.get_players():
        if player is not dealer:
            if player.calc_hand() == 21:
                print '%s: BLACKJACK!! CONGRATS!!' % (player.get_name())

            while player.calc_hand() < 21:
                print player_line(player) ## before
                user_in = raw_input('[H]it / [S]tand: ')
                if user_in is "H":
                    card = game.pull_card()
                    print 'HIT! [%s]' % (card)
                    player.addto_hand(card)
                elif user_in is "S":
                    print 'STAND!'
                    break

            if player.calc_hand() > 21:
                print 'BUST!'

    print '\n... playing the dealers hand ...'

    ## Play the dealer's hand..
    while dealer.calc_hand() < 21:
        print player_line(dealer)
        if dealer.calc_hand() < 17:
            card = game.pull_card()
            print 'HIT! [%s]' % (card)
            dealer.addto_hand(card)
        else:
            break

    print '\n... the final hands are ...'

    print player_line(dealer)
    dealer_hand = dealer.calc_hand()

    for player in game.get_players():
        if player is not dealer:
            print player_line(player, dealer_hand=dealer_hand)

if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print '\n[Keyboard Interrupt | QUITTING THE GAME..]'
