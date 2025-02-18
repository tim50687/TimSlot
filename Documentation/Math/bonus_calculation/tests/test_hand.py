import pytest
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from card import Card, Suits
from hand_evaluation import Hand, HandRank

class TestHand:
    def test_royal_flush(self):
        cards = [
            Card(14, Suits.HEARTS),  # Ace
            Card(13, Suits.HEARTS),  # King
            Card(12, Suits.HEARTS),  # Queen
            Card(11, Suits.HEARTS),  # Jack
            Card(10, Suits.HEARTS),  # 10
        ]
        hand = Hand(cards)
        assert hand.rank == HandRank.ROYAL_FLUSH
        assert hand.high_cards == []

    def test_straight_flush(self):
        cards = [
            Card(10, Suits.HEARTS),
            Card(9, Suits.HEARTS),
            Card(8, Suits.HEARTS),
            Card(7, Suits.HEARTS),
            Card(6, Suits.HEARTS),
        ]
        hand = Hand(cards)
        assert hand.rank == HandRank.STRAIGHT_FLUSH
        assert hand.high_cards == [10]

    def test_four_kind(self):
        cards = [
            Card(10, Suits.HEARTS),
            Card(10, Suits.DIAMONDS),
            Card(10, Suits.CLUBS),
            Card(10, Suits.SPADES),
            Card(7, Suits.HEARTS),
        ]
        hand = Hand(cards)
        assert hand.rank == HandRank.FOUR_KIND
        assert hand.high_cards == [10]

    def test_full_house(self):
        cards = [
            Card(10, Suits.HEARTS),
            Card(10, Suits.DIAMONDS),
            Card(10, Suits.CLUBS),
            Card(7, Suits.SPADES),
            Card(7, Suits.HEARTS),
        ]
        hand = Hand(cards)
        assert hand.rank == HandRank.FULL_HOUSE
        assert hand.high_cards == [10]

    def test_flush(self):
        cards = [
            Card(14, Suits.HEARTS),
            Card(10, Suits.HEARTS),
            Card(8, Suits.HEARTS),
            Card(7, Suits.HEARTS),
            Card(4, Suits.HEARTS),
        ]
        hand = Hand(cards)
        assert hand.rank == HandRank.FLUSH
        assert hand.high_cards == [14, 10, 8, 7, 4]

    def test_straight(self):
        # Regular straight
        cards = [
            Card(10, Suits.HEARTS),
            Card(9, Suits.DIAMONDS),
            Card(8, Suits.CLUBS),
            Card(7, Suits.SPADES),
            Card(6, Suits.HEARTS),
        ]
        hand = Hand(cards)
        assert hand.rank == HandRank.STRAIGHT
        assert hand.high_cards == [10]

        # Ace-low straight (A2345)
        cards = [
            Card(14, Suits.HEARTS),  # Ace
            Card(5, Suits.DIAMONDS),
            Card(4, Suits.CLUBS),
            Card(3, Suits.SPADES),
            Card(2, Suits.HEARTS),
        ]
        hand = Hand(cards)
        assert hand.rank == HandRank.STRAIGHT
        assert hand.high_cards == [5]  

    def test_three_kind(self):
        cards = [
            Card(10, Suits.HEARTS),
            Card(10, Suits.DIAMONDS),
            Card(10, Suits.CLUBS),
            Card(8, Suits.SPADES),
            Card(7, Suits.HEARTS),
        ]
        hand = Hand(cards)
        assert hand.rank == HandRank.THREE_KIND
        assert hand.high_cards == [10]

    def test_two_pair(self):
        cards = [
            Card(10, Suits.HEARTS),
            Card(10, Suits.DIAMONDS),
            Card(8, Suits.CLUBS),
            Card(8, Suits.SPADES),
            Card(7, Suits.HEARTS),
        ]
        hand = Hand(cards)
        assert hand.rank == HandRank.TWO_PAIR
        assert hand.high_cards == [10, 8, 7]

    def test_pair(self):
        cards = [
            Card(10, Suits.HEARTS),
            Card(10, Suits.DIAMONDS),
            Card(8, Suits.CLUBS),
            Card(7, Suits.SPADES),
            Card(6, Suits.HEARTS),
        ]
        hand = Hand(cards)
        assert hand.rank == HandRank.PAIR
        assert hand.high_cards == [10, 8, 7, 6]

    def test_high_card(self):
        cards = [
            Card(14, Suits.HEARTS),  # Ace
            Card(10, Suits.DIAMONDS),
            Card(8, Suits.CLUBS),
            Card(7, Suits.SPADES),
            Card(2, Suits.HEARTS),
        ]
        hand = Hand(cards)
        assert hand.rank == HandRank.HIGH_CARD
        assert hand.high_cards == [14, 10, 8, 7, 2]

    def test_hand_comparison(self):
        # Royal Flush beats everything
        royal_flush = Hand([
            Card(14, Suits.HEARTS),
            Card(13, Suits.HEARTS),
            Card(12, Suits.HEARTS),
            Card(11, Suits.HEARTS),
            Card(10, Suits.HEARTS),
        ])
        
        straight_flush = Hand([
            Card(13, Suits.HEARTS),
            Card(12, Suits.HEARTS),
            Card(11, Suits.HEARTS),
            Card(10, Suits.HEARTS),
            Card(9, Suits.HEARTS),
        ])
        
        assert straight_flush < royal_flush

    def test_same_rank_different_kickers(self):
        # Two pairs with different kickers
        hand1 = Hand([
            Card(10, Suits.HEARTS),
            Card(10, Suits.DIAMONDS),
            Card(8, Suits.CLUBS),
            Card(8, Suits.SPADES),
            Card(14, Suits.HEARTS),  # Ace kicker
        ])
        
        hand2 = Hand([
            Card(10, Suits.CLUBS),
            Card(10, Suits.SPADES),
            Card(8, Suits.HEARTS),
            Card(8, Suits.DIAMONDS),
            Card(2, Suits.CLUBS),   # 2 kicker
        ])
        
        assert hand2 < hand1  # hand1 wins due to Ace kicker

    def test_ace_low_straight(self):
        # A2345
        ace_low = Hand([
            Card(14, Suits.HEARTS),  # Ace
            Card(2, Suits.DIAMONDS),
            Card(3, Suits.CLUBS),
            Card(4, Suits.SPADES),
            Card(5, Suits.HEARTS),
        ])
        
        assert ace_low.rank == HandRank.STRAIGHT
        
        # Compare with 23456
        higher_straight = Hand([
            Card(6, Suits.HEARTS),
            Card(5, Suits.DIAMONDS),
            Card(4, Suits.CLUBS),
            Card(3, Suits.SPADES),
            Card(2, Suits.HEARTS),
        ])
        
        assert ace_low < higher_straight

    def test_full_house_comparison(self):
        # KKK88 vs KKK22
        hand1 = Hand([
            Card(13, Suits.HEARTS),  # King
            Card(13, Suits.DIAMONDS),
            Card(13, Suits.CLUBS),
            Card(8, Suits.SPADES),
            Card(8, Suits.HEARTS),
        ])
        
        hand2 = Hand([
            Card(12, Suits.SPADES),  # Queen
            Card(12, Suits.HEARTS),
            Card(12, Suits.DIAMONDS),
            Card(2, Suits.CLUBS),
            Card(2, Suits.SPADES),
        ])
        
        assert hand2 < hand1  # hand1 wins due to higher pair

    def test_invalid_hand_size(self):
        with pytest.raises(ValueError):
            Hand([Card(14, Suits.HEARTS), Card(13, Suits.HEARTS)])  # Too few cards
            
        with pytest.raises(ValueError):
            Hand([Card(14, Suits.HEARTS), Card(13, Suits.HEARTS), 
                Card(12, Suits.HEARTS), Card(11, Suits.HEARTS),
                Card(10, Suits.HEARTS), Card(9, Suits.HEARTS)])  # Too many cards

    def test_flush_comparison(self):
        # A♠ K♠ J♠ 9♠ 8♠ vs A♠ K♠ J♠ 9♠ 7♠
        hand1 = Hand([
            Card(14, Suits.SPADES),  # Ace
            Card(13, Suits.SPADES),  # King
            Card(11, Suits.SPADES),  # Jack
            Card(9, Suits.SPADES),
            Card(8, Suits.SPADES),
        ])
        
        hand2 = Hand([
            Card(14, Suits.SPADES),  # Ace
            Card(13, Suits.SPADES),  # King
            Card(11, Suits.SPADES),  # Jack
            Card(9, Suits.SPADES),
            Card(7, Suits.SPADES),
        ])
        
        assert hand2 < hand1