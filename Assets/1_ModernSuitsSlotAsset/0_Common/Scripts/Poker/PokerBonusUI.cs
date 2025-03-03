using UnityEngine;
using TMPro;
using UnityEngine.UI;

namespace PokerBonus
{
    public class PokerBonusUI : MonoBehaviour
    {
        public TextMeshProUGUI instructionText;
        public Button showHandButton;

        private void Start()
        {
            instructionText.text = "Pick one face-up card to change (only once) or keep your hand.";
            showHandButton.onClick.AddListener(OnShowHandClicked);
        }

        private void OnShowHandClicked()
        {
            FindObjectOfType<PokerBonusManager>().ShowHandsAndCompare();
        }

        public void ShowMessage(string message)
        {
            instructionText.text = message;
        }
    }
}
