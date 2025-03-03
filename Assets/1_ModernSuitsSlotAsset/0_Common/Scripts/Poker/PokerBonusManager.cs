using UnityEngine;
using UnityEngine.SceneManagement;
using System.Collections.Generic;

namespace PokerBonus
{

    /// <summary>
    /// Simple MonoBehaviour that uses the Deck and PokerHand classes
    /// to demonstrate a "bonus game" scenario.
    /// </summary>
    public class PokerBonusManager : MonoBehaviour
    {
        public Transform dealerCardsParent;
        public Transform playerCardsParent;
        public CardSpriteMapping cardSpriteMapping;
        public GameObject cardPrefab; 

        public Sprite cardBackSprite; 

        private List<Card> dealerCards;  // Create your own CardData class or use a similar structure
        private List<Card> playerCards;

        [Header("Poker Bonus Game Setup")]
        [Tooltip("Enter the name of the bonus scene to load")]
        public string nextSceneName = "BonusGameScene";

        private void Start()
        {
            Deck deck = new Deck();
            List<Card> playerCards = deck.Deal(5);
            List<Card> dealerCards = deck.Deal(5);

            for (int i = 0; i < dealerCards.Count; i++)
            {
                dealerCards[i].IsFaceUp = (i < 3); // reveal first 2 cards
            }
            for (int i = 0; i < playerCards.Count; i++)
            {
                playerCards[i].IsFaceUp = (i < 3);
            }

            DisplayCards(dealerCards, dealerCardsParent);
            DisplayCards(playerCards, playerCardsParent);
        }
        
        private void DisplayCards(List<Card> cards, Transform parent)
        {
            float xOffset = 5f;
            int index = 0;
            foreach (var card in cards)
            {
                GameObject cardObj = Instantiate(cardPrefab, parent);
                CardDisplay cd = cardObj.GetComponent<CardDisplay>();
                cd.rank = card.Rank;
                cd.suit = card.Suit;
                cd.isFaceUp = card.IsFaceUp;
                cd.SetCard(cardSpriteMapping.GetSprite(cd.rank, cd.suit));

                cardObj.transform.localPosition = new Vector3(index * xOffset, 0, 0);
                index++;
            }
        }
        

        /// <summary>
        /// Example method for loading the bonus scene
        /// </summary>
        public void LoadNextScene()
        {
            if (!string.IsNullOrEmpty(nextSceneName))
            {
                SceneManager.LoadScene(nextSceneName);
            }
            else
            {
                Debug.LogWarning("nextSceneName was not set!");
            }
        }
    }
}
