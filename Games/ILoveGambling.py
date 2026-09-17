"""
TODO

1: Create a simple 1 hand vs house blackjack game
    A Create a basic deck management system
    B Allow players to specifically be delt cards

2: Create interface using textual, keep it simple at first

3: Touch up visuals, make it look nice

4: Add poker with multiple 'players'

"""
import random

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
        self.__cards_in_play = []


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
        cards = self.__cards_in_play
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
        self.__cards_in_play.append(card)

    """Adds card to the discard pile
    
    Args:
        card(tuple): the card to discard
    """
    def DiscardCard(self, card: tuple):
        self.__cards_in_play.pop(self.__cards_in_play.index(card))
        self.__discard_pile.append(card)

    """Adds cards from the discard pile to the deck instance
        and shuffles them
    """
    def ShuffleDiscardPileAndUse(self):
        self.__deck_instance += self.__discard_pile
        self.ShuffleDeck()


class BlackJackPlayer():
    """Constructor for a player hand"""

    def __init__(self, player_name: str, cards: list, balance: int):
        self.__player_name = player_name
        self.__cards = cards
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
    def player_cards(self) -> list:
        return self.__cards

    @player_cards.setter
    def set_player_cards(self, cards: list):
        self.__cards = cards


class PlayBlackjack():
    """Main logic for playing and betting"""

    def __init__(self):
        self.manager = DeckManager()
        self.dealer = BlackJackPlayer("Dealer", [], 0)
        self.player = BlackJackPlayer("Player", [], 0)

    def Bet(self):
        pass

    def DealOut(self):
        pass

        

    

def main():
    pass


if __name__ == "__main__":
    main()