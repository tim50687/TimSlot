using UnityEngine;
using System.Runtime.InteropServices; // allow unity to call js function from WEBGL

namespace Mkey
{
public class GameController : MonoBehaviour
{   
    [DllImport("__Internal")] 
    private static extern void OnBalanceUpdated(string balance);

    private SlotPlayer MPlayer { get { return SlotPlayer.Instance; } }

    
    
    private void Start()
    {
        MPlayer.ChangeCoinsEvent -= OnPlayerBalanceChanged;
        MPlayer.ChangeCoinsEvent += OnPlayerBalanceChanged;
        #if UNITY_WEBGL && !UNITY_EDITOR
        WebGLInput.captureAllKeyboardInput = false;
        #endif
    }
    
    // Called from JavaScript/React when balance is set
    public void SetBalance(string balanceStr)
    {
        if (int.TryParse(balanceStr, out int balance))
        {
            Debug.Log($"Setting balance from React: {balance}");
            MPlayer.SetCoinsCount(balance);
        }
        else
        {
            Debug.LogError($"Failed to parse balance: {balanceStr}");
        }
    }
    
    // Called when SlotPlayer balance changes
    private void OnPlayerBalanceChanged(int newBalance)
    {
        Debug.Log($"Balance changed in game: {newBalance}");
        
        // Report back to React
        #if UNITY_WEBGL && !UNITY_EDITOR
        OnBalanceUpdated(newBalance.ToString());
        #else
        Debug.Log($"Would report balance to React: {newBalance}");
        #endif
    }
    
    private void OnDestroy()
    {
        // Unsubscribe to prevent memory leaks
        if (MPlayer != null)
            MPlayer.ChangeCoinsEvent -= OnPlayerBalanceChanged;
    }
}
}