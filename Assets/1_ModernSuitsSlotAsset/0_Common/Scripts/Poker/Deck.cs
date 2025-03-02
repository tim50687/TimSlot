using System;
using System.Collections.Generic;

namespace PokerBonus
{
    /// <summary>
    /// Represents a 52-card deck you can shuffle and deal from.
    /// </summary>
    public class Deck
    {
        private List<Card> cards;
        private System.Random rng = new System.Random();

        public Deck()
        {
            cards = new List<Card>();
            // Build full 52-card deck
            foreach (Suits suit in Enum.GetValues(typeof(Suits)))
            {
                for (int rank = 2; rank <= 14; rank++)
                {
                    cards.Add(new Card(rank, suit));
                }
            }
            Shuffle();
        }

        public void Shuffle()
        {
            // Fisher-Yates shuffle
            int n = cards.Count;
            for (int i = n - 1; i > 0; i--)
            {
                int k = rng.Next(i + 1);
                Card temp = cards[k];
                cards[k] = cards[i];
                cards[i] = temp;
            }
        }

        public List<Card> Deal(int count)
        {
            if (count > cards.Count)
                throw new Exception("Not enough cards in the deck!");

            List<Card> dealCards = cards.GetRange(0, count);
            cards.RemoveRange(0, count);
            return dealCards;
        }
    }
}
