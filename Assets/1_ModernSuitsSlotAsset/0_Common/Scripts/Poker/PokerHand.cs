using System;
using System.Collections.Generic;
using System.Linq;

namespace PokerBonus
{
    /// <summary>
    /// Evaluates a 5-card poker hand and determines its rank (Pair, Flush, etc.).
    /// </summary>
    public class PokerHand
    {
        public List<Card> Cards { get; private set; }   // exactly 5
        public HandRank Rank { get; private set; }
        public List<int> TieBreakValues { get; private set; } // for tie-breaking (e.g. kicker ranks)

        public PokerHand(List<Card> cards)
        {
            if (cards.Count != 5)
                throw new Exception("PokerHand must contain exactly 5 cards!");

            // Sort descending by rank
            Cards = cards.OrderByDescending(c => c.Rank).ToList();
            EvaluateHand();
        }

        private void EvaluateHand()
        {
            bool isFlush = IsFlush();
            bool isStraight = IsStraight(out int topStraightRank);
            bool isRoyal = (isFlush && isStraight && topStraightRank == 14);

            if (isRoyal)
            {
                Rank = HandRank.RoyalFlush;
                TieBreakValues = new List<int>();
                return;
            }
            if (isFlush && isStraight)
            {
                Rank = HandRank.StraightFlush;
                TieBreakValues = new List<int> { topStraightRank };
                return;
            }

            // Count occurrences of each rank
            var rankCount = Cards
                .GroupBy(c => c.Rank)
                .Select(g => new { Rank = g.Key, Count = g.Count() })
                .OrderByDescending(x => x.Count)
                .ThenByDescending(x => x.Rank)
                .ToList();

            // Four of a Kind?
            if (rankCount[0].Count == 4)
            {
                Rank = HandRank.FourOfKind;
                int fourRank = rankCount[0].Rank;
                int kicker = rankCount[1].Rank;
                TieBreakValues = new List<int> { fourRank, kicker };
                return;
            }

            // Full House?
            if (rankCount[0].Count == 3 && rankCount[1].Count == 2)
            {
                Rank = HandRank.FullHouse;
                int tripleRank = rankCount[0].Rank;
                int pairRank = rankCount[1].Rank;
                TieBreakValues = new List<int> { tripleRank, pairRank };
                return;
            }

            // Flush?
            if (isFlush)
            {
                Rank = HandRank.Flush;
                TieBreakValues = Cards.Select(c => c.Rank).ToList();
                return;
            }

            // Straight?
            if (isStraight)
            {
                Rank = HandRank.Straight;
                TieBreakValues = new List<int> { topStraightRank };
                return;
            }

            // Three of a Kind?
            if (rankCount[0].Count == 3)
            {
                Rank = HandRank.ThreeOfKind;
                int tripleRank = rankCount[0].Rank;
                var kickers = rankCount.Skip(1)
                    .Select(x => x.Rank)
                    .OrderByDescending(x => x)
                    .ToList();
                TieBreakValues = new List<int> { tripleRank };
                TieBreakValues.AddRange(kickers);
                return;
            }

            // Two Pair?
            if (rankCount[0].Count == 2 && rankCount[1].Count == 2)
            {
                Rank = HandRank.TwoPair;
                int highPair = rankCount[0].Rank;
                int lowPair = rankCount[1].Rank;
                int leftover = rankCount[2].Rank;
                TieBreakValues = new List<int> { highPair, lowPair, leftover };
                return;
            }

            // One Pair?
            if (rankCount[0].Count == 2)
            {
                Rank = HandRank.Pair;
                int pairRank = rankCount[0].Rank;
                var otherRanks = rankCount.Skip(1).Select(x => x.Rank).OrderByDescending(x => x).ToList();
                TieBreakValues = new List<int> { pairRank };
                TieBreakValues.AddRange(otherRanks);
                return;
            }

            // Else High Card
            Rank = HandRank.HighCard;
            TieBreakValues = Cards.Select(c => c.Rank).ToList();
        }

        private bool IsFlush()
        {
            Suits firstSuit = Cards[0].Suit;
            return Cards.All(c => c.Suit == firstSuit);
        }

        private bool IsStraight(out int topRank)
        {
            List<int> ranks = Cards.Select(c => c.Rank).ToList();
            for (int i = 0; i < ranks.Count - 1; i++)
            {
                if (ranks[i] - ranks[i + 1] != 1)
                {
                    // Check Ace-low: A 5 4 3 2
                    if (i == 0 && ranks[0] == 14 && ranks[1] == 5 && ranks[2] == 4 && ranks[3] == 3 && ranks[4] == 2)
                    {
                        topRank = 5; // Ace acts as 1
                        return true;
                    }
                    topRank = 0;
                    return false;
                }
            }
            topRank = ranks[0];
            return true;
        }

        public static bool operator <(PokerHand a, PokerHand b)
        {
            if (a.Rank != b.Rank) return a.Rank < b.Rank;
            for (int i = 0; i < a.TieBreakValues.Count; i++)
            {
                if (i >= b.TieBreakValues.Count) break;
                if (a.TieBreakValues[i] != b.TieBreakValues[i])
                    return a.TieBreakValues[i] < b.TieBreakValues[i];
            }
            return false;
        }
        public static bool operator >(PokerHand a, PokerHand b)
        {
            return !(a < b) && !a.Equals(b);
        }
    }
}
