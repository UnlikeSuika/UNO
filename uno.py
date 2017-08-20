from enum import Enum
import random
from random import shuffle


class CardColor(Enum):
    """Enumeration of colors of UNO cards."""
    RED = 1
    YELLOW = 2
    GREEN = 3
    BLUE = 4
    BLACK = 5


class CardType(Enum):
    """Enumeration of types of UNO cards."""
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    SKIP = 10
    REVERSE = 11
    DRAW_TWO = 12
    WILD = 13
    WILD_DRAW_FOUR = 14


class Card:
    """
    An UNO card.

    Attributes:
    color(CardColor)
    type (CardType)
    """
    def __init__(self, color, type):
        """
        Constructor of the card.

        Arguments:
        color(CardColor)
        type (CardType)
        """
        self.color = color
        self.type = type

    def __str__(self):
        """String representation of the card.

        Return:
        String
        """
        s = ""
        # Add the color of the card
        if self.color == CardColor["RED"]:
            s += "[R]"
        elif self.color == CardColor["YELLOW"]:
            s += "[Y]"
        elif self.color == CardColor["GREEN"]:
            s += "[G]"
        elif self.color == CardColor["BLUE"]:
            s += "[B]"
        # Add the type of the card
        if self.type == CardType["ZERO"]:
            s += "(0)"
        elif self.type == CardType["ONE"]:
            s += "(1)"
        elif self.type == CardType["TWO"]:
            s += "(2)"
        elif self.type == CardType["THREE"]:
            s += "(3)"
        elif self.type == CardType["FOUR"]:
            s += "(4)"
        elif self.type == CardType["FIVE"]:
            s += "(5)"
        elif self.type == CardType["SIX"]:
            s += "(6)"
        elif self.type == CardType["SEVEN"]:
            s += "(7)"
        elif self.type == CardType["EIGHT"]:
            s += "(8)"
        elif self.type == CardType["NINE"]:
            s += "(9)"
        elif self.type == CardType["SKIP"]:
            s += "(S)"
        elif self.type == CardType["REVERSE"]:
            s += "(R)"
        elif self.type == CardType["DRAW_TWO"]:
            s += "(D2)"
        elif self.type == CardType["WILD"]:
            s += "[W]"
        else:
            s += "[WD4]"
        return s

    def __repr__(self):
        """
        Repr representation of the card.

        Return:
        String
        """
        return self.__str__()
            
    def equals(self, card):
        """
        Determines if self is the same card as 'card'

        Argument:
        card(Card): card for comparing
        
        Return:
        bool
        """
        return (self.color == card.color and self.type == card.type)

    def equals_color(self, card):
        """
        Determines if self has the same color as 'card'

        Argument:
        card(Card): card for comparing

        Return:
        bool
        """
        return self.color == card.color

    def equals_type(self, card):
        """
        Determines if self has same type as 'card'

        Argument:
        card(Card): card for comparing

        Return:
        bool
        """
        return self.type == card.type

    def get_color(self):
        """
        Returns the color

        Return:
        CardColor
        """
        return self.color

    def get_type(self):
        """
        Returns the type

        Return:
        CardType
        """
        return self.type

    def get_compare_key(self):
        """
        Returns the key for comparing multiple cards

        Return:
        int
        """
        return self.color.value*100+self.type.value
        

class Player:
    """
    An UNO player.

    Attributes:
    cards(list of Card): UNO cards in hand
    score(int):          Score accumulated during the set of UNO games
    """
    def __init__(self):
        """Constructor of the player."""
        self.cards = []
        self.score = 0

    def receive_card(self, card):
        """
        Adds 'card' to the player's hand.

        Argument:
        card(Card)
        """
        self.cards.append(card)

    def discard_card(self, index):
        """
        Gets rid of player's card with given index.

        Argument:
        index(int)
        """
        del(self.cards[index])

    def print_cards(self):
        """Prints all cards the player has in hand."""
        index = 1
        for card in self.cards:
            print(str(index)+"."+str(card), end="  ")
            index += 1
        print()

    def get_cards(self):
        """
        Returns the list of cards the player has.
        
        Return: list of cards
        """
        return self.cards

    def shuffle_cards(self):
        """Shuffles the cards in hand."""
        shuffle(self.cards)

    def add_score(self, score):
        """
        Adds to the player's current score.

        Argument:
        score(int)
        """
        self.score += score

    def get_score(self):
        """
        Returns the player's current score.

        Return:
        int
        """
        return self.score

    def reset_cards(self):
        """Empties the player's current hand."""
        self.cards = []

    def sort_cards(self):
        """Sorts the player's current cards."""
        self.cards = sorted(self.cards, key=Card.get_compare_key)


class Game:
    """
    A single UNO game.

    Attributes:
    players     (list of Player): Players playing the game
    deck        (list of Card)  : Cards on deck
    discard     (list of Card)  : Pile of discarded cards
    wild_color  (CardColor)     : Color called upon playing wild card, or
                                  Black if no wild card is played
    winner_index(int)           : Index of the player who win the match, or
                                  -1 if the game has not ended yet
    clockwise   (bool)          : Whether to proceed to next turn in clockwise
                                  order. if false, then the order is
                                  counterclockwise.
    turn        (int)           : Index of the player who has the current turn
    """
    def __init__(self, players):
        """
        Constructor of Game.

        Argument:
        players(list of Player)
        """
        self.players = players
        self.deck = []
        self.discard = []
        self.wild_color = CardColor["BLACK"]
        self.winner_index = -1
        self.clockwise = True
        self.turn = 1
        self.__init_deck__()
        # Distribute seven cards to every player
        for player in self.players:
            player.reset_cards()
            for time in range(7):
                self.__give_topdeck_to_player__(player)
            player.sort_cards()
        # Discard a card from the top of the deck
        self.__discard_topdeck__()
        # If the discarded card is Wild Draw Four, shuffle and discard again
        while self.discard[-1].equals(Card(CardColor["BLACK"],
                                           CardType["WILD_DRAW_FOUR"])):
            self.deck.append(self.discard[-1])
            del(self.discard[-1])
            self.__shuffle_deck__()
            self.__discard_topdeck__()
        # Cases where the first discard is an action card
        if self.discard[-1].get_type() == CardType["SKIP"]:
            self.__next_turn__()
        elif self.discard[-1].get_type() == CardType["DRAW_TWO"]:
            self.__give_topdeck_to_player__(self.players[self.turn])
            self.__give_topdeck_to_player__(self.players[self.turn])
            self.players[self.turn].sort_cards()
            self.__next_turn__()
        elif self.discard[-1].get_type() == CardType["REVERSE"]:
            self.clockwise = False
            self.__next_turn__()
        elif self.discard[-1].get_type() == CardType["WILD"]:
            print("Discarded card is a wild card. Choose a color by \".<first "
                  +"letter of color>\" format (without quotations).")
            called_color = input().lower()
            while called_color not in [".r", ".y", ".g", ".b"]:
                print("Invalid input. Choose one from \".r\", \".y\", \".g\", "
                      +"and \".b\" (without quotations).")
                calledColor = input().lower()
            i = [".r", ".y", ".g", ".b"].index(called_color)
            self.wild_color = CardColor(i+1)

    def __init_deck__(self):
        """Fill the deck with a full deck of UNO cards."""
        # Add the colored cards
        for color in range(1, 5):
            self.deck.append(Card(CardColor(color), CardType["ZERO"]))
            for type in range(1, 13):
                for time in range(2):
                    self.deck.append(Card(CardColor(color), CardType(type)))
        # Add Wild cards and Wild Draw Four cards
        for time in range(4):
            self.deck.append(Card(CardColor["BLACK"], CardType["WILD"]))
            self.deck.append(Card(CardColor["BLACK"],
                                  CardType["WILD_DRAW_FOUR"]))
        self.__shuffle_deck__()

    def __shuffle_deck__(self):
        """Shuffles the current deck"""
        shuffle(self.deck)

    def __give_topdeck_to_player__(self, player):
        """
        Adds the top card from the deck to player's hand.

        Argument:
        player(Player): The player receiving the topdeck
        """
        # Move discarded cards to the deck if the deck is empty
        if not self.deck:
            self.deck = self.discard[:-1]
            self.__shuffle_deck__()
            self.discard = [self.discard[-1]]
            # Ran out of cards from deck/discard, so player can't draw
            if not self.deck:
                print("Deck is empty. Player could not draw.")
                return False
        player.receive_card(self.deck[-1])
        del(self.deck[-1])
        return True

    def __discard_topdeck__(self):
        """Discard the top card from the deck."""
        self.discard.append(self.deck[-1])
        del(self.deck[-1])

    def __discard_player_card__(self, player, card_index):
        """
        Discard the player's card with the given index.

        Argument:
        player    (Player): The player from whom the card is to be discarded
        card_index(int)   : The index of the card to discard
        """
        self.discard.append(player.get_cards()[card_index])
        player.discard_card(card_index)

    def __next_turn__(self):
        """Proceed to the next player's turn."""
        if self.clockwise:
            self.turn += 1
            if self.turn >= len(self.players):
                self.turn -= len(self.players)
        else:
            self.turn -= 1
            if self.turn < 0:
                self.turn += len(self.players)

    def __can_be_played__(self, card):
        """
        Determines if the card can currently be played.

        Return:
        bool: True if the card can be played, False otherwise
        """
        if (self.wild_color != CardColor["BLACK"]
                and card.get_color() == self.wild_color):
            return True
        elif card.equals_color(self.discard[-1]):
            return True
        if card.equals_type(self.discard[-1]):
            return True
        if card.get_color() == CardColor["BLACK"]:
            return True
    
    def __play_card__(self, index):
        """
        Play the card of the given index, and move on to the next turn.

        Argument:
        index(int): Index of the card

        Return:
        bool: False if the current player wins the match, True otherwise
        """
        card = self.players[self.turn].get_cards()[index]
        self.__discard_player_card__(self.players[self.turn], index)
        turn_before = self.turn
        # Skip card
        if card.get_type() == CardType["SKIP"]:
            self.__next_turn__()
            print("Player "+str(self.turn+1)+" is skipped.")
            self.__next_turn__()
            self.wild_color == CardColor["BLACK"]
        # Draw Two card
        elif card.get_type() == CardType["DRAW_TWO"]:
            self.__next_turn__()
            self.__give_topdeck_to_player__(self.players[self.turn])
            self.__give_topdeck_to_player__(self.players[self.turn])
            print("Player "
                  +str(self.turn+1)
                  +" draws "
                  +str(self.players[self.turn].get_cards()[-2])
                  +", "
                  +str(self.players[self.turn].get_cards()[-1])
                  +" and is skipped.")
            self.players[self.turn].sort_cards()
            self.__next_turn__()
            self.wild_color == CardColor["BLACK"]
        # Reverse card
        elif card.get_type() == CardType["REVERSE"]:
            # Acts the same way as Skip card if there are only two players
            if len(self.players) == 2:
                self.__next_turn__()
                print("Player "+str(self.turn+1)+" is skipped.")
                self.__next_turn__()
            else:
                print("Order is reversed.")
                if self.clockwise:
                    self.clockwise = False
                else:
                    self.clockwise = True
                self.__next_turn__()
            self.wild_color == CardColor["BLACK"]
        # Wild card
        elif card.get_type() == CardType["WILD"]:
            print("Choose a color for wild card (\".r\", \".y\", \".g\", or \""
                  +".b\")")
            color = input().split()[0]
            while color not in [".r", ".y", ".g", ".b"]:
                print("Invalid input.")
                color = input().split()[0]
            color_value = [".r", ".y", ".g", ".b"].index(color) + 1
            self.wild_color = CardColor(color_value)
            self.__next_turn__()
        # Wild Draw Four card
        elif card.get_type() == CardType["WILD_DRAW_FOUR"]:
            # Determine if Wild Draw Four card is legal
            is_legal_wd4 = True
            for card_it in self.players[self.turn].get_cards():
                if card_it.get_type() == CardType['WILD_DRAW_FOUR']:
                    continue
                elif (self.discard[-2].get_color() == CardColor['BLACK']
                      and card_it.get_color == self.wild_color):
                    is_legal_wd4 = False
                    break
                elif (self.discard[-2].get_color() != CardColor['BLACK']
                      and card_it.equals_color(self.discard[-2])):
                    is_legal_wd4 = False
                    break
            # Choose colour for wild
            print("Choose a color for wild card (\".r\", \".y\", \".g\", or \"."
                  +"b\")")
            color = input().split()[0]
            while color not in [".r", ".y", ".g", ".b"]:
                print("Invalid input.")
                color = input().split()[0]
            color_value = [".r", ".y", ".g", ".b"].index(color) + 1
            self.wild_color = CardColor(color_value)
            challenged_index = self.turn
            # Gives next player an opportunity to challenge
            self.__next_turn__()
            print("Will Player "
                  +str(self.turn+1)
                  + " challenge the Wild Draw Four?")
            print("Answer by yes (\".y\") or no (\".n\").")
            answer = input().split()[0]
            while answer not in [".y", ".n"]:
                print("Invalid input.")
                answer = input().split()[0]
            # If challenged
            if answer == ".y":
                print("Player "+str(challenged_index+1)+"'s cards are:")
                self.players[challenged_index].print_cards()
                self.players[challenged_index].shuffle_cards()
                # If challenge is not successful
                if is_legal_wd4:
                    print("The Wild Draw Four was legal.")            
                    print("Player "+str(self.turn+1)+" draws ", end="")
                    for i in range(6):
                        self.__give_topdeck_to_player__(self.players[self.turn])
                        print(str(self.players[self.turn].get_cards()[-1]),
                              end="")
                        if i < 5:
                            print(", ", end="")
                    print(" and is skipped.")
                    self.players[self.turn].sort_cards()
                # If challenge is successful
                else:
                    print("The Wild Draw Four was illegal.")
                    print("Player "+str(challenged_index+1)+" draws ", end="")
                    for i in range(4):
                        self.__give_topdeck_to_player__(
                            self.players[challenged_index])
                        print(
                            str(self.players[challenged_index].get_cards()[-1]),
                            end="")
                        if i < 3:
                            print(", ", end="")
                    print(".\nPlayer "+str(self.turn+1)+" is skipped.")
                    self.players[challenged_index].sort_cards()
            # If not challenged
            else:
                print("Player "+str(self.turn+1)+" draws ", end="")
                for i in range(4):
                    self.__give_topdeck_to_player__(self.players[self.turn])
                    print(str(self.players[self.turn].get_cards()[-1]), end="")
                    if i < 3:
                        print(", ", end="")
                print(" and is skipped.")
                self.players[self.turn].sort_cards()
            self.__next_turn__()
        # A non-action card
        else:
            self.__next_turn__()
        # If the player wins the match
        if not self.players[turn_before].get_cards():
            self.winner_index = turn_before
            return False
        return True

    def run(self):
        """Ask the current player what to do, and move on to the next turn.

        Return:
        bool: False if the game has ended this turn, True otherwise
        """
        print("----------")
        print("Player "+str(self.turn+1)+"'s turn.")
        self.players[self.turn].print_cards()
        print("Top card: "+str(self.discard[-1]), end="")
        # Print the color called for Wild card (if applicable)
        if self.discard[-1].get_color() == CardColor["BLACK"]:
            if self.wild_color == CardColor["RED"]:
                print("[R]", end="")
            elif self.wild_color == CardColor["YELLOW"]:
                print("[Y]", end="")
            elif self.wild_color == CardColor["GREEN"]:
                print("[G]", end="")
            else:
                print("[B]", end="")
        print("\nPlay a card by \".p <card index>\" or draw by \".d\" (without "
              +"quotations).")
        # Loop continues until player makes a valid input.
        while True:
            move = input().split()
            if not move:
                print("Invalid input.")
            # Case of playing a card
            elif move[0] == ".p":
                if len(move) < 2:
                    print("Invalid input.")
                    continue
                try:
                    index = int(eval(move[1])) - 1
                except KeyboardInterrupt:
                    return
                except:
                    print("Invalid input.")
                    continue
                if index < 0 or index >= len(
                  self.players[self.turn].get_cards()):
                    print("Index out of range.")
                    continue
                player_card = self.players[self.turn].get_cards()[index]
                if self.__can_be_played__(player_card):
                    return self.__play_card__(index)
                else:
                    print("This card cannot be played.")
                    continue
            # Case of drawing a card
            elif move[0] == ".d":
                if not self.__give_topdeck_to_player__(self.players[self.turn]):
                    self.__next_turn__()
                    return True
                new_card = self.players[self.turn].get_cards()[-1]
                print("You have drawn card: "+str(new_card))
                print("Keep(\".k\") or play(\".p\")?")
                choice = input()
                while choice.split()[0] not in [".k", ".p"]:
                    print("Invalid input.")
                    choice = input()
                # Only play the card if the card can be played
                if choice.split()[0] == ".p":
                    if self.__can_be_played__(new_card):
                        return self.__play_card__(-1)
                    else:
                        print("This card cannot be played.")
                self.players[self.turn].sort_cards()
                self.__next_turn__()
                return True
            else:
                print("Invalid input.")

    def game_end(self):
        """
        Add the score to the winner

        Return:
        int: Index of the player who wins the game
        """
        score = 0
        winner = self.players[self.winner_index]
        for player in self.players:
            if player == winner:
                continue
            for card in player.get_cards():
                if card.get_type() == CardType["ONE"]:
                    score += 1
                elif card.get_type() == CardType["TWO"]:
                    score += 2
                elif card.get_type() == CardType["THREE"]:
                    score += 3
                elif card.get_type() == CardType["FOUR"]:
                    score += 4
                elif card.get_type() == CardType["FIVE"]:
                    score += 5
                elif card.get_type() == CardType["SIX"]:
                    score += 6
                elif card.get_type() == CardType["SEVEN"]:
                    score += 7
                elif card.get_type() == CardType["EIGHT"]:
                    score += 8
                elif card.get_type() == CardType["NINE"]:
                    score += 9
                elif card.get_type() in [CardType["SKIP"],
                                         CardType["DRAW_TWO"],
                                         CardType["REVERSE"]]:
                    score += 20
                elif card.get_type() in [CardType["WILD"],
                                         CardType["WILD_DRAW_FOUR"]]:
                    score += 50
        self.players[self.winner_index].add_score(score)
        print("Player "
              +str(self.winner_index+1)
              +" earns "
              +str(score)
              +" points!")
        return self.winner_index


def main():
    print("How many players? (2-10)")
    while True:
        try:
            num_player = int(eval(input()))
            if num_player >= 2 and num_player <= 10:
                break
            else:
                print("There must be two to ten players.")
        except KeyboardInterrupt:
            return
        except:
            print("Invalid input.")
    players = []
    for i in range(num_player):
        players.append(Player())
    game = Game(players)
    while True:
        if not game.run():
            winner_index = game.game_end()
            print("===== Current scoreboard =====")
            for i in range(len(players)):
                if i == winner_index:
                    print("*", end="")
                print("Player "+str(i+1)+": "+str(players[i].get_score()))
            print("==============================")
            winner = players[winner_index]
            if winner.get_score() >= 500:
                print("Player "
                      +str(winner_index+1)
                      +" wins with total score of "
                      +str(winner.get_score())
                      +"!")
                return
            else:
                print("Starting next game...")
                game = Game(players)

main()
