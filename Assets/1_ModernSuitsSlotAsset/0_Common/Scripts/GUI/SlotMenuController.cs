using System.Collections;
using UnityEngine;
using UnityEngine.UI;

namespace Mkey
{
    public class SlotMenuController : MonoBehaviour
    {
        // Add extra spacing aboe this field in Unity Inspector
        [Space(16, order = 0)]
        [SerializeField]
        private SlotController slot;

        #region temp vars
        private Button[] buttons;
        #endregion temp vars

        #region regular
        void Start()
        {
            // Finds and stores all Buttons components that are children of this GameObject
            buttons = GetComponentsInChildren<Button>(true);
        }
        #endregion regular

        /// <summary>
        /// Set all buttons interactble = activity
        /// </summary>
        /// <param name="activity"></param>
        public void SetControlActivity(bool activity)
        {
            if (buttons == null) return;
            foreach (Button b in buttons)
            {
              if(b)  b.interactable = activity;
            }
        }

        private string GetMoneyName(int count)
        {
            if (count > 1) return "coins";
            else return "coin";
        }
    }
}