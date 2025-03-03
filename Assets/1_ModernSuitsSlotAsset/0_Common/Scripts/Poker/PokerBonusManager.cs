using UnityEngine;
using UnityEngine.SceneManagement;
using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using Mkey;

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

        public Text balanceText;
        private int newBalance = 0;

        public Sprite cardBackSprite; 

        private List<Card> dealerCards;  // Create your own CardData class or use a similar structure
        private List<Card> playerCards;

        [Header("Poker Bonus Game Setup")]
        [Tooltip("Enter the name of the bonus scene to load")]
        public string nextSceneName = "BonusGameScene";

        private Deck deck;

        private bool hasSwitchedCard = false;

        [Header("Poker Bonus Game Setup")]
        public string previousSceneName = "3_Slot_3X3"; // Set this to your slot scene


        private Dictionary<HandRank, int> multipliers = new Dictionary<HandRank, int>
        {
            { HandRank.RoyalFlush, 100000 },
            { HandRank.StraightFlush, 10000 },
            { HandRank.FourOfKind, 1000 },
            { HandRank.FullHouse, 500 },
            { HandRank.Flush, 300 },
            { HandRank.Straight, 100 },
            { HandRank.ThreeOfKind, 50 },
            { HandRank.TwoPair, 25 },
            { HandRank.Pair, 5 },
            { HandRank.HighCard, 3 }
        };

        private void Start()
        {
            deck = new Deck();
            playerCards = deck.Deal(5);
            dealerCards = deck.Deal(5);

            for (int i = 0; i < dealerCards.Count; i++)
            {
                dealerCards[i].IsFaceUp = (i < 3); // reveal first 2 cards
            }
            for (int i = 0; i < playerCards.Count; i++)
            {
                playerCards[i].IsFaceUp = (i < 3);
            }

            DisplayCards(dealerCards, dealerCardsParent, false);
            DisplayCards(playerCards, playerCardsParent, true);
        }
        
        private void DisplayCards(List<Card> cards, Transform parent, bool allowSwitch)
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
                cd.cardIndex = index;
                cd.isSwitchable = allowSwitch;
                cd.SetCard(cardSpriteMapping.GetSprite(cd.rank, cd.suit));

                cardObj.transform.localPosition = new Vector3(index * xOffset, 0, 0);
                index++;
            }
        }

        /// <summary>
        /// Allows player to switch one face-up card at most once.
        /// </summary>
        public void TrySwitchCard(int index, GameObject cardObj)
        {
            if (hasSwitchedCard)
            {
                FindObjectOfType<PokerBonusUI>().ShowMessage("You can only switch once!");
                return;
            }

            Card newCard = deck.Deal(1)[0]; // Draw one new card
            playerCards[index] = newCard;
            newCard.IsFaceUp = true;

            // Update UI
            CardDisplay cd = cardObj.GetComponent<CardDisplay>();
            cd.rank = newCard.Rank;
            cd.suit = newCard.Suit;
            cd.isFaceUp = true;
            cd.SetCard(cardSpriteMapping.GetSprite(cd.rank, cd.suit));

            hasSwitchedCard = true;
            FindObjectOfType<PokerBonusUI>().ShowMessage("You switched a card!");
        }

        /// <summary>
        /// Called when the "Show Hand" button is pressed.
        /// </summary>
        public void ShowHandsAndCompare()
        {
            // Flip all remaining face-down cards
            foreach (Transform child in dealerCardsParent)
            {
                CardDisplay cd = child.GetComponent<CardDisplay>();
                cd.isFaceUp = true;
                cd.SetCard(cardSpriteMapping.GetSprite(cd.rank, cd.suit));
            }
            foreach (Transform child in playerCardsParent)
            {
                CardDisplay cd = child.GetComponent<CardDisplay>();
                cd.isFaceUp = true;
                cd.SetCard(cardSpriteMapping.GetSprite(cd.rank, cd.suit));
            }

            CompareHands();
        }

        private void CompareHands()
        {
            PokerHand playerHand = new PokerHand(playerCards);
            PokerHand dealerHand = new PokerHand(dealerCards);

            if (playerHand > dealerHand)
            {
                int winnings = 1 * multipliers[playerHand.Rank]; // Adjust multiplier
                // get the balance from text
                int balance = int.Parse(balanceText.text.Replace(",", ""));
                newBalance = balance + winnings;
                UpdateBalanceUI();
                FindObjectOfType<PokerBonusUI>().ShowMessage($"You Win! You earned {winnings} coins. Returning to Slot Game...");
                SlotPlayer.Instance.AddCoins(winnings);
            }
            else if (playerHand < dealerHand)
            {
                FindObjectOfType<PokerBonusUI>().ShowMessage("You Lose! Returning to Slot Game...");
            }
            else
            {
                FindObjectOfType<PokerBonusUI>().ShowMessage("It's a Tie! Returning to Slot Game...");
            }

            StartCoroutine(ReturnToPreviousScene());
        }

        private void UpdateBalanceUI()
        {
            if (balanceText != null)
            {
                balanceText.text = $"{newBalance}";
            }
        }

        private IEnumerator ReturnToPreviousScene()
        {
            yield return new WaitForSeconds(3f);
            SceneManager.LoadScene(previousSceneName);
        }
    }
}
