using System.Collections.Generic;
using UnityEngine;

namespace PokerBonus
{
[System.Serializable]
public class CardSpriteEntry
{
    public int rank;   // 2-14
    public Suits suit;
    public Sprite faceSprite;
}

// Maps each card's rank and suit to its sprite image.
public class CardSpriteMapping : MonoBehaviour
{
    public List<CardSpriteEntry> cardSprites;

    private Dictionary<string, Sprite> spriteDict;

    void Awake()
    {
        spriteDict = new Dictionary<string, Sprite>();
        foreach (var entry in cardSprites)
        {
            string key = GetKey(entry.rank, entry.suit);
            if (!spriteDict.ContainsKey(key))
                spriteDict.Add(key, entry.faceSprite);
        }
    }

    public Sprite GetSprite(int rank, Suits suit)
    {
        string key = GetKey(rank, suit);
        if (spriteDict.ContainsKey(key))
            return spriteDict[key];
        return null;
    }

    private string GetKey(int rank, Suits suit)
    {
        return rank.ToString() + "_" + suit.ToString();
    }
}

}