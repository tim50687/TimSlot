from card import Card, Suits
from hand_evaluation import Hand, HandRank
from typing import List, Optional
from collections import defaultdict

class RespinStrategy:
    def choose_respin(self, player_up_cards: List[Card], player_down_cards: List[Card], 
                    dealer_up_cards: List[Card]):
        """
        Determines which card (if any) to respin based on player and dealer visible cards
        
        Args:
            player_up_cards: The 3 face-up cards of the player
            player_down_cards: The 2 face-down cards of the player (known to player)
            dealer_up_cards: The 3 face-up cards of the dealer
            
        Returns:
            Card to respin or None if no respin recommended
        """

        if self._has_protected_hand(player_up_cards):
            return None
        
        if self._has_pair_in_cards(player_up_cards):
            return self._get_pair_respin_card(player_up_cards, dealer_up_cards)
        
        if self._has_flush_draw_in_up_cards(player_up_cards) or self._has_straight_draw_in_up_cards(player_up_cards):
            return self._get_drawing_hand_respin(player_up_cards)
        
        # High card situation
        return self._get_high_card_respin(player_up_cards, dealer_up_cards)
    
    def _has_protected_hand(self, up_cards: List[Card]) -> bool:
        ranks = [card.rank for card in up_cards]
        suits = [card.suit for card in up_cards]
        # Check if it's 3 of a kind already
        if len(set(ranks)) == 1:
            return True
        
        # Check if all same suits
        if len(set(suits)) == 1:
            return True

        # Check if 3 consecutive cards
        sorted_rank = sorted(ranks)
        if sorted_rank[2] - sorted_rank[1] == 1 and sorted_rank[1] - sorted_rank[0] == 1:
            return True
        
        # Check for the case for A, 2, 3
        if sorted_rank == [2, 3, 14]:
            return True
        
        return False
            

    def _has_pair_in_cards(self, up_cards: List[Card]) -> bool:
        ranks = [card.rank for card in up_cards]
        for rank in ranks:
            if ranks.count(rank) >= 2:
                return True
        return False

    def _get_pair_respin_card(self, up_cards: List[Card], 
                            dealer_up_cards: List[Card]) -> Optional[Card]:
        """Determine which card to respin if player has a pair in face-up cards"""
        ranks = [card.rank for card in up_cards]

        # Try to find out the unique rank
        unique_rank = 0
        for rank in ranks:
            unique_rank = unique_rank ^ rank

        # Get dealor highest then compare with it
        dealer_highest = max(card.rank for card in dealer_up_cards)

        if unique_rank > dealer_highest:
            return None
        
        # return the unique rank card
        for card in up_cards:
            if card.rank == unique_rank:
                return card
            
        return None

    def _has_flush_draw_in_up_cards(self, up_cards: List[Card]) -> bool:
        """Check if face-up cards have 2 cards of the same suit"""
        suits = [card.suit for card in up_cards]
        for suit in suits:
            if suits.count(suit) >= 2:
                return True
        return False
    
    def _has_straight_draw_in_up_cards(self, up_cards: List[Card]) -> bool:
        """Check if face-up cards have at least 2 consecutive cards"""
        ranks = sorted(card.rank for card in up_cards)
        if ranks[1] - ranks[0] == 1 or ranks[2] - ranks[1] == 1:
            return True

        # Deal with A, 2
        if 14 in ranks and 2 in ranks:
            return True
        
        return False

    def _get_drawing_hand_respin(self, up_cards: List[Card]) -> Optional[Card]:
        """Determine which card to respin for drawing hand"""
        # deal with flush draw
        if self._has_flush_draw_in_up_cards(up_cards):
            suits_count = defaultdict(int)
            for card in up_cards:
                suits_count[card.suit] += 1

            flush_suit = max(suits_count, key= lambda x: suits_count[x])

            for card in up_cards:
                if card.suit != flush_suit:
                    return card
                
        # deal with straight draw
        if self._has_straight_draw_in_up_cards(up_cards):
            ranks = [card.rank for card in up_cards]

            # Case for A, 2
            if 14 in ranks and 2 in ranks:
                for card in up_cards:
                    if card.rank != 14 and card.rank != 2:
                        return card
            sorted_cards_by_rank = sorted(up_cards, key= lambda c: c.rank)
            if sorted_cards_by_rank[1].rank - sorted_cards_by_rank[0].rank == 1:
                return sorted_cards_by_rank[2]
            if sorted_cards_by_rank[2].rank - sorted_cards_by_rank[1].rank == 1:
                return sorted_cards_by_rank[0]
        
        # Fallback
        return self._get_high_card_respin(up_cards, [])


    def _get_high_card_respin(self, up_cards: List[Card], 
                            dealer_cards: List[Card]) -> Card:
        """In high card situations, respin the lowest card
        unless it's higher than dealer's highest"""
        
        sorted_player_up_cards = sorted(up_cards, key=lambda c: c.rank)
        player_lowest = sorted_player_up_cards[0]

        # Check if lowest card is higher than 10
        if player_lowest.rank >= 10:
            return None
        
        # Check against dealer
        if dealer_cards:
            dealer_highest = max(card.rank for card in dealer_cards)
            if player_lowest.rank > dealer_highest:
                return None
        
        return player_lowest

