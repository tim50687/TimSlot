using UnityEngine;
using UnityEngine.UI;
using UnityEngine.EventSystems;

namespace PokerBonus
{
public class CardDisplay : MonoBehaviour, IPointerClickHandler
{
    public int rank;
    public Suits suit;
    public bool isFaceUp = true;

    private Image cardImage;

    // A sprite for the card back (assigned via Inspector or via a manager)
    public Sprite cardBackSprite;

    public int cardIndex;

    private PokerBonusManager bonusManager;
    public bool isSwitchable = false;

    void Awake()
    {
        cardImage = GetComponent<Image>(); 
        bonusManager = FindObjectOfType<PokerBonusManager>(); 
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

    public void OnPointerClick(PointerEventData eventData)
        {
            if (isFaceUp && isSwitchable) // Can only switch face-up cards
            {
                bonusManager.PlayCardClickSound();
                bonusManager.TrySwitchCard(cardIndex, gameObject);
            }
        }
}
}