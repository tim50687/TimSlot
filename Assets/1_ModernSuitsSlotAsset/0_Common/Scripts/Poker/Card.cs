using System;

namespace PokerBonus
{
    /// <summary>
    /// Represents a single playing card with a rank (2..14) and suit (Hearts, Spades, Diamonds, Clubs).
    /// </summary>
    [Serializable]
    public class Card
    {
        public int Rank;     // 2..14, where 11=J, 12=Q, 13=K, 14=A
        public Suits Suit;   // Hearts, Spades, Diamonds, Clubs
        public bool IsFaceUp = true;

        public Card(int rank, Suits suit)
        {
            Rank = rank;
            Suit = suit;
        }

        public override string ToString()
        {
            // Convert numeric rank to e.g. "J" or "K"
            switch (Rank)
            {
                case 11: return $"J of {Suit}";
                case 12: return $"Q of {Suit}";
                case 13: return $"K of {Suit}";
                case 14: return $"A of {Suit}";
                default: return $"{Rank} of {Suit}";
            }
        }
    }
}
