using UnityEngine;
using UnityEngine.UI;

namespace PokerBonus
{
public class CardDisplay : MonoBehaviour
{
    public int rank;
    public Suits suit;
    public bool isFaceUp = true;

    private Image cardImage;

    // A sprite for the card back (assigned via Inspector or via a manager)
    public Sprite cardBackSprite;


    void Awake()
    {
        cardImage = GetComponent<Image>(); // or GetComponent<SpriteRenderer>() if using that
    }

    public void SetCard(Sprite faceSprite)
    {
        if (isFaceUp)
        {
            cardImage.sprite = faceSprite;
        }
        else
        {
            cardImage.sprite = cardBackSprite;
        }
    }
}
}