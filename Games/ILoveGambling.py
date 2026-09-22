"""
TODO

1: Create a simple 1 hand vs house blackjack game
    A Create a basic deck management system DONE
    B Allow players to specifically be delt cards 

2: Create interface using textual, keep it simple at first

3: Touch up visuals, make it look nice

4: Add poker with multiple 'players'

"""
import random
import time
import os

# Close this
# Gonna keep it as a dict for now as it lets me add extra data
# like an image name later on when things get more complicated
deck = [
    ("Ace", "Spades"), ("2", "Spades"), ("3", "Spades"), ("4", "Spades"), ("5", "Spades"),
    ("6", "Spades"), ("7", "Spades"), ("8", "Spades"), ("9", "Spades"), ("10", "Spades"),
    ("Jack", "Spades"), ("Queen", "Spades"), ("King", "Spades"),
    ("Ace", "Hearts"), ("2", "Hearts"), ("3", "Hearts"), ("4", "Hearts"), ("5", "Hearts"),
    ("6", "Hearts"), ("7", "Hearts"), ("8", "Hearts"), ("9", "Hearts"), ("10", "Hearts"),
    ("Jack", "Hearts"), ("Queen", "Hearts"), ("King", "Hearts"),
    ("Ace", "Diamonds"), ("2", "Diamonds"), ("3", "Diamonds"), ("4", "Diamonds"), ("5", "Diamonds"),
    ("6", "Diamonds"), ("7", "Diamonds"), ("8", "Diamonds"), ("9", "Diamonds"), ("10", "Diamonds"),
    ("Jack", "Diamonds"), ("Queen", "Diamonds"), ("King", "Diamonds"),
    ("Ace", "Clubs"), ("2", "Clubs"), ("3", "Clubs"), ("4", "Clubs"), ("5", "Clubs"),
    ("6", "Clubs"), ("7", "Clubs"), ("8", "Clubs"), ("9", "Clubs"), ("10", "Clubs"),
    ("Jack", "Clubs"), ("Queen", "Clubs"), ("King", "Clubs")
]
class DeckManager():
    """Handles the shuffling and dealing of cards from the deck."""

    def __init__(self):
        self.__deck_instance = deck.copy()
        self.__discard_pile = []
        self.__hand_in_play = []


    """Selects the top card from the self.__deck_instance
        Removes it from the deck, and adds its to cards in play
    
    Returns:
        str: The card selected
    """
    def DealCard(self) -> str:
        if len(self.__deck_instance) > 0:
            card = self.__deck_instance.pop() # Technically this is like taking the bottom card but its not really a physical deck so whatever
            self.AddCardToPlay(card)
            return card
        else:
            raise ValueError("No cards left to draw!")

    """Shuffles the self.__deck_instance"""
    def ShuffleDeck(self):
        for i in range(200):
            index1 = random.randint(0, len(self.__deck_instance) - 1)
            index2 = random.randint(0, len(self.__deck_instance) - 1)
            self.__deck_instance[index1], self.__deck_instance[index2] = self.__deck_instance[index2], self.__deck_instance[index1]

    """Getter for deck instance
    
    Returns:
        deck(list): A list of the cards in the undelt-deck
    """
    @property
    def GetDeckInstance(self) -> list:
        deck = self.__deck_instance
        return deck

    """Gets cards that are in play
    
    Returns:
        cards(list): Cards that are currently in play
    """
    @property
    def GetCardsInPlay(self) -> list:
        cards = self.__hand_in_play
        return cards

    """Gets all cards in the discard pile
    
    Returns:
        cards(list): Cards that are in the discard pile
    """
    @property
    def GetDiscardedCards(self) -> list:
        cards = self.__discard_pile
        return cards

    """Adds a card to play
    
    Args:
        card(tuple): the card to add
    """
    def AddCardToPlay(self, card: tuple):
        self.__hand_in_play.append(card)


    """Moves cards that are currently in play to the discard pile.
        Example use, when a round or hand is over and must be redelt
    """
    def RemoveCardsInPlay(self):
        self.__discard_pile.append(self.__hand_in_play)
        self.__hand_in_play = []

    """Adds card to the discard pile
    
    Args:
        card(tuple): the card to discard
    """
    def DiscardCard(self, card: tuple):
        self.__hand_in_play.pop(self.__hand_in_play.index(card))
        self.__discard_pile.append(card)

    """Adds cards from the discard pile to the deck instance
        and shuffles them
    """
    def ShuffleDiscardPileAndUse(self):
        self.__deck_instance += self.__discard_pile
        self.ShuffleDeck()


    """Prints ascii art of a card

    Args:
        card(tuple): The card to display, reads value and suit as (value, suit)
    
    Returns:
        str: The printed card
    """
    def CardPrinter(self, card: tuple) -> str:
        value = card[0]
        suit = card[1]
        suit_art = {
            "Hearts": (" /\\ /\\ ", "(      )", " \\    / ", "  \\  /  ", "   \\/   "),
            "Diamonds": ("    /\\   ", "   /  \\  ", "  <    > ", "   \\  /  ", "    \\/   "),
            "Clubs": ("   ____  ", "  (    ) ", " (  ()  )", "   \\__/  ", "    ||   "),
            "Spades": ("    /\\   ", "   /  \\  ", "  (    ) ", "   \\  /  ", "    ||   "),
        }.get(suit, (suit, "", "", "", ""))

        return f"""
+---------+
| {value:<7} |
|{suit_art[0]:^9}|
|{suit_art[1]:^9}|
|{suit_art[2]:^9}|
|{suit_art[3]:^9}|
|{suit_art[4]:^9}|
| {value:>7} |
+---------+
"""


class BlackJackPlayer():
    """Used to instantiate the player and dealer"""

    def __init__(self, player_name: str, hand: list, balance: int):
        self.__player_name = player_name
        self.__hand = hand
        self.__balance = balance

    @property
    def player_name(self) -> str:
        return self.__player_name

    @player_name.setter
    def player_name(self, value: str):
        self.__player_name = value

    @property
    def balance(self) -> int:
        return self.__balance

    @balance.setter
    def balance(self, value: int):
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self.__balance = value    

    @property
    def player_hand(self) -> list:
        return self.__hand

    @player_hand.setter
    def player_hand(self, hand: list):
        self.__hand = hand


class PlayBlackjack():
    """Main logic for playing and betting"""

    def __init__(self):
        self.dealer = BlackJackPlayer("Dealer", [], 0)
        self.player = BlackJackPlayer("Player", [], 1000)
        self.player_bet = 0
        self.game_state = "player_betting"
        self.DeckManager = DeckManager()
        self.player_total = 0
        self.dealer_total = 0

    """Changes the Blackjack game state
    
    Args:
        new_state(str): The state to change too

    Raises:
        ValueError: If new_state is not a valid state
    """
    def SetState(self, new_state: str):
        valid_states = {
            "player_betting",
            "initial_deal",
            "player_turn",
            "dealer_turn",
            "game_over",
        }
        if new_state not in valid_states:
            raise ValueError(
                f"Invalid game state: {new_state!r}. "
                f"Expected one of {sorted(valid_states)}"
            )
        self.game_state = new_state

    """Prompts the player for their bet.

    Raises:
        ValueError: If the amount input is not an int, or if the amount
                    input is greater then the balance
    """
    def Bet(self):
        if self.player.balance < 1:
            print("Game Over!")
            self.SetState("game_over")
        else:
            while True:
                print("Place your bet for this hand.")
                print(f"Balance: {self.player.balance}")
                amount = input("Place your bet: ")
                try:

                    self.player_bet = int(amount)

                    if int(amount) < 0 or int(amount) > self.player.balance:
                        raise ValueError
                    self.DeckManager.RemoveCardsInPlay()
                    self.player.player_hand = []
                    self.dealer.player_hand = []
                    self.SetState("initial_deal")
                    break
                except ValueError as e:
                    print(f"Please place a valid integer as a bet that is not negative and is not greater then your balance")

    """Deals out the initial 4 cards of a hand"""
    def InitialDeal(self):
        try:
            # Shuffle
            self.DeckManager.ShuffleDeck()

            # Dealer First Card
            self.dealer.player_hand.append(self.DeckManager.DealCard())

            # Player First Card
            self.player.player_hand.append(self.DeckManager.DealCard())

            # Dealer Second Card
            self.dealer.player_hand.append(self.DeckManager.DealCard())

            # Player Second Card
            self.player.player_hand.append(self.DeckManager.DealCard())

            self.SetState("player_turn")
        except ValueError as e:
            print(e)

    """Prints all the cards in play. Hides dealer bottom card
    
    Args:
        dealer_shows_cards(bool): Toggles if the dealer bottom card is shown
    """
    def PrintTable(self, dealer_shows_cards: bool = False):
        os.system('cls' if os.name == 'nt' else 'clear')

        print(f" {"Dealer Cards:":>7}")
        if not dealer_shows_cards:
            dealer_card_rows = [
                self.DeckManager.CardPrinter(card).strip("\n").splitlines()
                for card in (self.dealer.player_hand[0], ("","") )
            ]
        else:
            dealer_card_rows = [
                self.DeckManager.CardPrinter(card).strip("\n").splitlines()
                for card in self.dealer.player_hand
            ]
        dealer_cards_display = "\n".join(
            "  ".join(row)
            for row in zip(*dealer_card_rows)
        )
        print(dealer_cards_display + "\n")


        print(f" {"Player Cards:":>7}")
        card_rows = [
            self.DeckManager.CardPrinter(card).strip("\n").splitlines()
            for card in self.player.player_hand
        ]
        players_card_display = "\n".join(
            "  ".join(row)
            for row in zip(*card_rows)
        )

        print(players_card_display)

    """The hit/stand loop"""
    def PlayerDecision(self):
        # Calculate Sum, if 21, give 1.5X bet reward
        # Offer the ability to Hit, Split(Add later), Or Pass
        # Loop until player busts or selects pass
        try:
            while True:
                self.PrintTable()
                # If dealer upcard is valued at 10 or is an Ace check
                self.dealer_total = 0
                for each in self.dealer.player_hand:
                    if each[0] == "Ace":
                        if (self.dealer_total + 11) > 21:
                            self.dealer_total = self.dealer_total + 1
                        else:
                            self.dealer_total = self.dealer_total + 11
                    elif (each[0] == "King" or 
                        each[0] == "Queen" or
                        each[0] == "Jack"):
                        self.dealer_total = self.dealer_total + 10

                    else:
                        self.dealer_total = self.dealer_total + int(each[0])

                if self.dealer_total == 21:
                    self.PrintTable(True)
                    print("Dealer has 21, player loses")
                    self.player.balance = self.player.balance - self.player_bet
                    time.sleep(5)
                    self.SetState("player_betting")
                    break

                # Redo the count everyloop so it properly updates ace values
                self.player_total = 0
                for each in self.player.player_hand:
                    if each[0] == "Ace":
                        if (self.player_total + 11) > 21:
                            print("Ace is counted as 1")
                            self.player_total = self.player_total + 1
                        else:
                            self.player_total = self.player_total + 11
                    elif (each[0] == "King" or 
                        each[0] == "Queen" or
                        each[0] == "Jack"):
                        self.player_total = self.player_total + 10

                    else:
                        self.player_total = self.player_total + int(each[0])

                if self.player_total > 21:
                    print(f"Player busted and lost ${self.player_bet}")
                    self.player.balance = self.player.balance - self.player_bet
                    time.sleep(5)
                    self.SetState("player_betting")
                    break

                print(f"Player total is {self.player_total}")
                choice = None
                while True:
                    try:
                        print("Hit(1) or Stand(2):")
                        choice = input("")
                        choice = int(choice)
                        if choice not in (1, 2):
                            raise ValueError
                        break
                    except ValueError:
                        print("Please select 1 or 2")
            
                if choice == 2:
                    self.SetState("dealer_turn")
                    break
                elif choice == 1:
                    self.player.player_hand.append(self.DeckManager.DealCard())

        except Exception as e:
            print(e)

    """Dealer hits after player stands"""
    def DealerHits(self):
        try:
            while True:
                self.PrintTable(True)

                self.dealer_total = 0
                for each in self.dealer.player_hand:
                    if each[0] == "Ace":
                        if (self.dealer_total + 11) > 21:
                            self.dealer_total = self.dealer_total + 1
                        else:
                            self.dealer_total = self.dealer_total + 11
                    elif (each[0] == "King" or 
                        each[0] == "Queen" or
                        each[0] == "Jack"):
                        self.dealer_total = self.dealer_total + 10

                    else:
                        self.dealer_total = self.dealer_total + int(each[0])

                print(f"Dealer has {self.dealer_total}")
                print(f"The player has {self.player_total}")
                if self.dealer_total < 17:
                    self.dealer.player_hand.append(self.DeckManager.DealCard())
                    time.sleep(2)
                elif self.dealer_total > 21:
                    print(f"The dealer busts! The player wins ${self.player_bet}")
                    self.player.balance = self.player.balance + (self.player_bet*2)
                    time.sleep(5)
                    self.SetState("player_betting")
                    break
                else:
                    if self.dealer_total > self.player_total:
                        self.player.balance = self.player.balance - self.player_bet
                        print(f"The dealer wins this hand, the player loses ${self.player_bet}")
                    elif self.player_total > self.dealer_total:
                        self.player.balance = self.player.balance + (self.player_bet*2)
                        print(f"The player wins this hand and wins ${self.player_bet}")
                    else:
                        print("Draw!")

                    time.sleep(5)
                    self.SetState("player_betting")
                    break

        except Exception as e:
            print(e)
            time.sleep(5)
            self.SetState("player_betting")

def main():
    BlackJack = PlayBlackjack()

    while True:
        match BlackJack.game_state:
            case "player_betting":
                os.system('cls' if os.name == 'nt' else 'clear')
                BlackJack.Bet()
            case "initial_deal":
                BlackJack.InitialDeal()
            case "player_turn":
                BlackJack.PlayerDecision()
            case "dealer_turn":
                BlackJack.DealerHits()
            case "game_over":
                break


if __name__ == "__main__":
    main()