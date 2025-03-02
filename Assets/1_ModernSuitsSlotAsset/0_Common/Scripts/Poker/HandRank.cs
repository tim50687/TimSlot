namespace PokerBonus
{
    /// <summary>
    /// Enumeration of standard poker hand strengths, from HighCard (lowest) to RoyalFlush (highest).
    /// </summary>
    public enum HandRank
    {
        HighCard = 1,
        Pair,
        TwoPair,
        ThreeOfKind,
        Straight,
        Flush,
        FullHouse,
        FourOfKind,
        StraightFlush,
        RoyalFlush
    }
}
