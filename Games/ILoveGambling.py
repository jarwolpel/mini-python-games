"""
TODO

1: Create interface using textual, keep it simple at first

2: Create a simple 1 hand vs house blackjack game

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
    """Handles the shuffling and dealing of cards from the deck.
        This will be used for all card games.
    """

    def __init__(self):
        self.__deckInstance = deck.copy()


    """Selects the top card from the self.__deckInstance, pops it, and returns it.
    
    Returns:
        str: The card selected

    """
    def dealCard(self) -> str:
        pass

    """Shuffles the self.__deckInstance"""
    def ShuffleDeck(self):
        for i in range(200):
            index1 = random.randint(0, len(self.__deckInstance) - 1)
            index2 = random.randint(0, len(self.__deckInstance) - 1)
            self.__deckInstance[index1], self.__deckInstance[index2] = self.__deckInstance[index2], self.__deckInstance[index1]

    """Prints self.__deckInstance. This is for debugging purposes"""
    def ShowDeck(self):
        for i, card in enumerate(self.__deckInstance):
            print(f"{i+1}: {card[0]} of {card[1]}")


class BlackJackHand():
    """Contains functions necessary to hit, stand, split, and bust"""

    def __init__(self):
        pass

class PlayBlackjack():
    """Main logic for playing and betting"""

    def __init__(self):
        self.DeckManager = DeckManager()

def main():
    manager = DeckManager()
    manager.ShuffleDeck()
    manager.ShowDeck()


if __name__ == "__main__":
    main()