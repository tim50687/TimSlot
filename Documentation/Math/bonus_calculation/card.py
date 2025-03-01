from enum import Enum
import random


class Suits(Enum):
    HEARTS = "H"
    SPADES = "S"
    DIAMONDS = "D"
    CLUBS = "C"

class Card:
    def __init__(self, rank, suit: Suits):
        self.rank = rank
        self.suit = suit
        self.is_face_up = True

    def __str__(self):
        ranks = {11: "J", 12: "Q", 13: "K", 14: "A"}
        rank_str = ranks.get(self.rank, str(self.rank))
        return f"{rank_str} of {self.suit.value}"

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank
    
    def __lt__(self, other):
        return self.rank < other.rank
    
    def __repr__(self):
        ranks = {11: "J", 12: "Q", 13: "K", 14: "A"}
        rank_str = ranks.get(self.rank, str(self.rank))
        return f"{rank_str} of {self.suit.value}"

class Deck:
    def __init__(self):
        self.cards = [
            Card(rank, suit)
            for suit in Suits
            for rank in range(2, 15)
        ]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, n):
        if n > len(self.cards):
            raise ValueError("Not enough cards")
        dealt = self.cards[:n]
        self.cards = self.cards[n:]
        return dealt
    
    def __str__(self):
        card_str = ""
        for card in self.cards:
            card_str += str(card) + " "
        return card_str.strip()
