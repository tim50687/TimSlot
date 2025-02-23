using UnityEngine;
using System; // This imports .NET standard library

public enum Suit
{
    Hearts,
    Spades,
    Diamonds,
    Clubs
}

[System.Serializable]
public class Card : MonoBehaviour // Script can be attached to a GameObject
{
    public int rank;
    public Suit suit;
    public bool isFaceUp = true;
    
    // Use SpriteRenderer component for displaying 2D images
    [SerializeField] private SpriteRenders spriteRenders;
    [SerializeField] private Sprite cardBack;
    [SerializeField] private Sprite[] cardFaces;
}