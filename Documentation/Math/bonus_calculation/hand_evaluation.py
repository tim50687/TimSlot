from enum import Enum
from collections import Counter
from card import Card, Suits


class HandRank(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

    def __lt__(self, other):
        return self.value < other.value
    
class Hand:
    def __init__(self, cards):
        if len(cards) != 5:
            raise ValueError("Hand must contain exactly 5 cards")
        self.cards = sorted(cards, key=lambda x: x.rank, reverse=True)
        self.rank, self.high_cards = self._evaluate_hand()

    def _evaluate_hand(self):
        """
        Evaluates the poker hand and returns (HandRank, [high cards])
        High cards are used for breaking ties (list of value used to compare)
        """
        if self._is_royal_flush():
            return HandRank.ROYAL_FLUSH, [] # no need to compare high cards for royal flush
        
        if self._is_straight_flush():
            return HandRank.STRAIGHT_FLUSH, [self.cards[0].rank] 
        
        if self._is_four_kind():
            return HandRank.FOUR_KIND, self._get_four_kind_kickers()
        
        if self._is_full_house():
            return HandRank.FULL_HOUSE, self._get_full_house_kickers()
        
        if self._is_flush():
            return HandRank.FLUSH, [c.rank for c in self.cards]
        
        if self._is_straight():
            return HandRank.STRAIGHT, self._get_straight_kickers()
        
        if self._is_three_kind():
            return HandRank.THREE_KIND, self._get_three_kind_kickers()
        
        if self._is_two_pair():
            return HandRank.TWO_PAIR, self._get_two_pair_kickers()
        
        if self._is_pair():
            return HandRank.PAIR, self._get_pair_kickers()
        
        return HandRank.HIGH_CARD, [c.rank for c in self.cards]
    
    def _is_royal_flush(self):
        return self._is_straight_flush() and self.cards[0].rank == 14
    
    def _is_straight_flush(self):
        return self._is_flush() and self._is_straight()

    def _is_four_kind(self):
        ranks_count = Counter(c.rank for c in self.cards)
        return 4 in ranks_count.values()
    
    def _is_full_house(self):
        ranks_count = Counter(c.rank for c in self.cards)
        return 3 in ranks_count.values() and 2 in ranks_count.values()
    
    def _is_flush(self):
        return len(set(card.suit for card in self.cards)) == 1
    
    def _is_straight(self):
        ranks = [card.rank for card in self.cards]
        if self._is_sequential(ranks):
            return True
        # check for A, 2, 3, 4, 5
        return ranks == [14, 5, 4, 3, 2]
    
    def _is_sequential(self, ranks):
        return all(ranks[i] - ranks[i + 1] == 1 for i in range(len(self.cards) - 1))
    
    def _is_three_kind(self):
        rank_counts = Counter(card.rank for card in self.cards)
        return 3 in rank_counts.values()
    
    def _is_two_pair(self) -> bool:
        rank_counts = Counter(card.rank for card in self.cards)
        return list(rank_counts.values()).count(2) == 2
    
    def _is_pair(self) -> bool:
        rank_counts = Counter(card.rank for card in self.cards)
        return 2 in rank_counts.values()
    
    def _get_straight_kickers(self):
        rank = [card.rank for card in self.cards]
        if rank == [14, 5, 4, 3, 2]:
            return [5]
        return [rank[0]]
    
    def _get_four_kind_kickers(self):
        rank_counts = Counter(card.rank for card in self.cards)
        four_rank = [r for r, c in rank_counts.items() if c == 4]
        return four_rank

    def _get_full_house_kickers(self):
        rank_counts = Counter(card.rank for card in self.cards)
        three_rank = [r for r, c in rank_counts.items() if c == 3]
        return three_rank

    def _get_three_kind_kickers(self):
        rank_counts = Counter(card.rank for card in self.cards)
        three_rank = [r for r, c in rank_counts.items() if c == 3]
        return three_rank

    def _get_two_pair_kickers(self):
        rank_counts = Counter(card.rank for card in self.cards)
        pairs = sorted([r for r, c in rank_counts.items() if c == 2], reverse=True)
        kicker = [r for r, c in rank_counts.items() if c == 1]
        return pairs + kicker

    def _get_pair_kickers(self):
        rank_counts = Counter(card.rank for card in self.cards)
        pair_rank = [r for r, c in rank_counts.items() if c == 2][0]
        kickers = sorted([r for r in rank_counts if r != pair_rank], reverse=True)
        return [pair_rank] + kickers

    def __lt__(self, other):
        if self.rank != other.rank:
            print(self.rank)
            return self.rank < other.rank

        for self_rank, other_rank in zip(self.high_cards, other.high_cards):
            if self_rank != other_rank:
                return self_rank < other_rank
            
        return False