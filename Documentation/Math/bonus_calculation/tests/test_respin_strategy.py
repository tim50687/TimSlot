import pytest
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from card import Card, Suits
from strategy import RespinStrategy

class TestRespinStrategy:
    def setup_method(self):
        self.strategy = RespinStrategy()
        # Common dealer cards for testing
        self.dealer_medium = [
            Card(10, Suits.HEARTS),
            Card(8, Suits.CLUBS),
            Card(6, Suits.DIAMONDS)
        ]
        
    def test_protected_hand_three_of_a_kind(self):
        """Test that three of a kind is protected (no respin)"""
        up_cards = [
            Card(10, Suits.HEARTS),
            Card(10, Suits.CLUBS),
            Card(10, Suits.DIAMONDS)
        ]
        down_cards = [
            Card(2, Suits.SPADES),
            Card(3, Suits.HEARTS)
        ]
        
        result = self.strategy.choose_respin(up_cards, down_cards, self.dealer_medium)
        assert result is None, "Three of a kind should be protected"
        
    def test_protected_hand_flush_draw(self):
        """Test that three cards of same suit are protected"""
        up_cards = [
            Card(10, Suits.HEARTS),
            Card(5, Suits.HEARTS),
            Card(2, Suits.HEARTS)
        ]
        down_cards = [
            Card(2, Suits.SPADES),
            Card(3, Suits.CLUBS)
        ]
        
        result = self.strategy.choose_respin(up_cards, down_cards, self.dealer_medium)
        assert result is None, "Three to flush should be protected"
        
    def test_protected_hand_straight(self):
        """Test that three consecutive cards are protected"""
        up_cards = [
            Card(10, Suits.HEARTS),
            Card(9, Suits.CLUBS),
            Card(8, Suits.DIAMONDS)
        ]
        down_cards = [
            Card(2, Suits.SPADES),
            Card(3, Suits.HEARTS)
        ]
        
        result = self.strategy.choose_respin(up_cards, down_cards, self.dealer_medium)
        assert result is None, "Three consecutive cards should be protected"
        
    def test_protected_hand_ace_low_straight(self):
        """Test that A-2-3 straight is protected"""
        up_cards = [
            Card(14, Suits.HEARTS),  # Ace
            Card(2, Suits.CLUBS),
            Card(3, Suits.DIAMONDS)
        ]
        down_cards = [
            Card(7, Suits.SPADES),
            Card(8, Suits.HEARTS)
        ]
        
        result = self.strategy.choose_respin(up_cards, down_cards, self.dealer_medium)
        assert result is None, "A-2-3 straight should be protected"
    
    def test_pair_respin_basic(self):
        """Test that with pair, third card is marked for respin"""
        up_cards = [
            Card(10, Suits.HEARTS),
            Card(10, Suits.CLUBS),
            Card(5, Suits.DIAMONDS)
        ]
        down_cards = [
            Card(2, Suits.SPADES),
            Card(3, Suits.HEARTS)
        ]
        
        result = self.strategy.choose_respin(up_cards, down_cards, self.dealer_medium)
        assert result == up_cards[2], "Third card should be marked for respin"
        
    def test_pair_respin_high_kicker(self):
        """Test that with pair and high kicker (higher than dealer's highest), no respin"""
        up_cards = [
            Card(10, Suits.HEARTS),
            Card(10, Suits.CLUBS),
            Card(12, Suits.DIAMONDS)  # Queen, higher than dealer's highest (10)
        ]
        down_cards = [
            Card(2, Suits.SPADES),
            Card(3, Suits.HEARTS)
        ]
        
        result = self.strategy.choose_respin(up_cards, down_cards, self.dealer_medium)
        assert result is None, "High kicker should not be respun when higher than dealer's highest"
        
    def test_pair_respin_three_of_a_kind(self):
        """Test that with three of a kind, XOR approach handles it correctly"""
        up_cards = [
            Card(10, Suits.HEARTS),
            Card(10, Suits.CLUBS),
            Card(10, Suits.DIAMONDS)
        ]
        down_cards = [
            Card(2, Suits.SPADES),
            Card(3, Suits.HEARTS)
        ]
        
        # This should be caught by protected hand check first, but testing XOR logic
        result = self.strategy.choose_respin(up_cards, down_cards, self.dealer_medium)
        assert result is None, "Three of a kind should be protected"
        
    def test_flush_draw_respin(self):
        """Test respin logic for flush draw"""
        up_cards = [
            Card(10, Suits.HEARTS),
            Card(5, Suits.HEARTS),
            Card(7, Suits.CLUBS)
        ]
        down_cards = [
            Card(2, Suits.SPADES),
            Card(3, Suits.HEARTS)
        ]
        
        result = self.strategy.choose_respin(up_cards, down_cards, self.dealer_medium)
        assert result == up_cards[2], "Non-heart card should be marked for respin"
        
    def test_flush_draw_three_suits(self):
        """Test flush draw with one card of each suit"""
        up_cards = [
            Card(10, Suits.HEARTS),
            Card(5, Suits.CLUBS),
            Card(7, Suits.DIAMONDS)
        ]
        down_cards = [
            Card(2, Suits.SPADES),
            Card(3, Suits.HEARTS)
        ]
        
        # Should fall back to high card logic
        result = self.strategy.choose_respin(up_cards, down_cards, self.dealer_medium)
        assert result == up_cards[1], "Lowest card should be respun in high card situation"
        
    def test_straight_draw_consecutive_first_two(self):
        """Test straight draw with first two cards consecutive"""
        up_cards = [
            Card(7, Suits.HEARTS),
            Card(8, Suits.CLUBS),
            Card(10, Suits.DIAMONDS)
        ]
        down_cards = [
            Card(2, Suits.SPADES),
            Card(3, Suits.HEARTS)
        ]
        
        result = self.strategy.choose_respin(up_cards, down_cards, self.dealer_medium)
        assert result == up_cards[2], "Non-consecutive card should be respun"
        
    def test_straight_draw_consecutive_last_two(self):
        """Test straight draw with last two cards consecutive"""
        up_cards = [
            Card(5, Suits.HEARTS),
            Card(9, Suits.CLUBS),
            Card(10, Suits.DIAMONDS)
        ]
        down_cards = [
            Card(2, Suits.SPADES),
            Card(3, Suits.HEARTS)
        ]
        
        result = self.strategy.choose_respin(up_cards, down_cards, self.dealer_medium)
        assert result == up_cards[0], "Non-consecutive card should be respun"
        
    def test_straight_draw_ace_two(self):
        """Test A-2 straight draw scenario"""
        up_cards = [
            Card(14, Suits.HEARTS),  # Ace
            Card(2, Suits.CLUBS),
            Card(10, Suits.DIAMONDS)
        ]
        down_cards = [
            Card(7, Suits.SPADES),
            Card(8, Suits.HEARTS)
        ]
        
        result = self.strategy.choose_respin(up_cards, down_cards, self.dealer_medium)
        assert result == up_cards[2], "Non A/2 card should be respun"
        
    def test_high_card_basic(self):
        """Test basic high card scenario - respin lowest"""
        up_cards = [
            Card(12, Suits.HEARTS),  # Queen
            Card(9, Suits.CLUBS),
            Card(5, Suits.DIAMONDS)
        ]
        down_cards = [
            Card(7, Suits.SPADES),
            Card(8, Suits.HEARTS)
        ]
        
        result = self.strategy.choose_respin(up_cards, down_cards, self.dealer_medium)
        assert result == up_cards[2], "Lowest card should be respun"
        
    def test_high_card_high_lowest(self):
        """Test high card where lowest is still high (>10)"""
        up_cards = [
            Card(14, Suits.HEARTS),  # Ace
            Card(12, Suits.CLUBS),   # King  
            Card(10, Suits.DIAMONDS) # TEN
        ]
        down_cards = [
            Card(7, Suits.SPADES),
            Card(8, Suits.HEARTS)
        ]
        
        result = self.strategy.choose_respin(up_cards, down_cards, self.dealer_medium)
        assert result is None, "No respin when lowest card is high"
        
    def test_high_card_higher_than_dealer(self):
        """Test high card where lowest is higher than dealer's highest"""
        dealer_low = [
            Card(5, Suits.HEARTS),
            Card(3, Suits.CLUBS),
            Card(2, Suits.DIAMONDS)
        ]
        
        up_cards = [
            Card(10, Suits.HEARTS),
            Card(8, Suits.CLUBS),
            Card(6, Suits.DIAMONDS) # Higher than dealer's highest (5)
        ]
        down_cards = [
            Card(2, Suits.SPADES),
            Card(3, Suits.HEARTS)
        ]
        
        result = self.strategy.choose_respin(up_cards, down_cards, dealer_low)
        assert result is None, "No respin when lowest card beats dealer's highest"
        
    def test_edge_case_pair_with_high_third(self):
        """Test edge case: pair with high third card compared to dealer"""
        dealer_low = [
            Card(5, Suits.HEARTS),
            Card(3, Suits.CLUBS),
            Card(2, Suits.DIAMONDS)
        ]
        
        up_cards = [
            Card(4, Suits.HEARTS),
            Card(4, Suits.CLUBS),
            Card(7, Suits.DIAMONDS) # Higher than dealer's highest (5)
        ]
        down_cards = [
            Card(2, Suits.SPADES),
            Card(3, Suits.HEARTS)
        ]
        
        result = self.strategy.choose_respin(up_cards, down_cards, dealer_low)
        assert result is None, "No respin when kicker beats dealer's highest"
        
    def test_edge_case_three_distinct_suits(self):
        """Test edge case: three different suits"""
        up_cards = [
            Card(10, Suits.HEARTS),
            Card(8, Suits.CLUBS),
            Card(6, Suits.DIAMONDS)
        ]
        down_cards = [
            Card(2, Suits.SPADES),
            Card(3, Suits.HEARTS)
        ]
        
        # Should fall back to high card strategy
        result = self.strategy.choose_respin(up_cards, down_cards, self.dealer_medium)
        assert result == up_cards[2], "Lowest card should be respun"
        
    def test_edge_case_no_dealer_cards(self):
        """Test edge case: no dealer cards provided"""
        up_cards = [
            Card(10, Suits.HEARTS),
            Card(8, Suits.CLUBS),
            Card(6, Suits.DIAMONDS)
        ]
        down_cards = [
            Card(2, Suits.SPADES),
            Card(3, Suits.HEARTS)
        ]
        
        result = self.strategy.choose_respin(up_cards, down_cards, [])
        assert result == up_cards[2], "Should default to lowest card with no dealer cards"
        
    def test_edge_case_face_cards(self):
        """Test edge case with face cards"""
        up_cards = [
            Card(13, Suits.HEARTS),  # King
            Card(12, Suits.CLUBS),   # Queen
            Card(11, Suits.DIAMONDS) # Jack
        ]
        down_cards = [
            Card(2, Suits.SPADES),
            Card(3, Suits.HEARTS)
        ]
        
        result = self.strategy.choose_respin(up_cards, down_cards, self.dealer_medium)
        assert result is None, "No respin when all cards are face cards"
        
    def test_mixed_scenario(self):
        """Test mixed scenario with both flush and straight potential"""
        up_cards = [
            Card(10, Suits.HEARTS),
            Card(9, Suits.HEARTS),
            Card(7, Suits.CLUBS)
        ]
        down_cards = [
            Card(2, Suits.SPADES),
            Card(3, Suits.HEARTS)
        ]
        
        # Has both flush draw (2 hearts) and straight draw (9-10)
        # Should prioritize flush draw due to order of checks
        result = self.strategy.choose_respin(up_cards, down_cards, self.dealer_medium)
        assert result == up_cards[2], "Should respin the non-hearts card"