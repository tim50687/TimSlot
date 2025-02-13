using UnityEngine;

public class GameManager : MonoBehaviour
{

    public static GameManager Instance { get; private set; }
    
    [SerializeField] private SlotManager slotManager;
    [SerializeField] private UIManager uiManager;
    
    private void Awake()
    {
        // Singleton pattern setup
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }
    
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        // Initialize game state
        InitializeGame();
    }

    private void InitializeGame()
    {
        // TODO: Set up initial game state
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
