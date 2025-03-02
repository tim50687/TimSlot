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
        [Header("Poker Bonus Game Setup")]
        [Tooltip("Enter the name of the bonus scene to load")]
        public string nextSceneName = "BonusGameScene";

        private void Start()
        {
            // Example: deal & evaluate two 5-card hands automatically
            TestBonusRound();
        }

        /// <summary>
        /// Deals a player hand and dealer hand, compares them, and logs the results.
        /// This is just a simple demonstration you can expand in your own UI.
        /// </summary>
        public void TestBonusRound()
        {
            Deck deck = new Deck();
            List<Card> playerCards = deck.Deal(5);
            List<Card> dealerCards = deck.Deal(5);

            PokerHand playerHand = new PokerHand(playerCards);
            PokerHand dealerHand = new PokerHand(dealerCards);

            Debug.Log("Player has: " + string.Join(", ", playerCards) + " => " + playerHand.Rank);
            Debug.Log("Dealer has: " + string.Join(", ", dealerCards) + " => " + dealerHand.Rank);

            bool playerWins = (playerHand > dealerHand);
            if (playerWins)
                Debug.Log("PLAYER WINS!");
            else
                Debug.Log("PLAYER LOSES!");
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
