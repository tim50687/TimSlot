## 0. Prize Pool

- Royal Flush: 10x prize pool (Odds: 0.000154%)
- Straight Flush: 5x prize pool (Odds: 0.00139%)
- Four of a Kind: 4x prize pool (Odds: 0.0240%)
- Full House: 3.5x prize pool (Odds: 0.1441%)
- Flush: 3x prize pool (Odds: 0.1965%)
- Straight: 2x prize pool (Odds: 0.3925%)
- Three of a Kind: 1.5x prize pool (Odds: 2.1128%)
- Two Pair: 1.2x prize pool (Odds: 4.7539%)
- Pair: 1x prize pool (Odds: 42.2569%)
- High Card: 1x prize pool (Odds: 50.1177%)


## 1. Set Up the Model

1. **Deck and Dealing Sequence**  
   - A single standard 52‐card deck.  
   - The Dealer is dealt 5 cards (3 face up, 2 face down).  
   - The Player is dealt 5 cards (3 face up, 2 face down).

2. **Information**  
   - The Player sees *their own* 5 cards (3 up, 2 down) plus the **3 face‐up** Dealer cards.  
   - The Player does **not** see the Dealer’s 2 face‐down cards.

3. **Player’s One Re‐Spin**  
   - The Player may choose to re‐spin *one* of their 3 face‐up cards exactly once (or decline altogether).  
   - “Re‐spin” means discarding that face‐up card and drawing a new card from the remaining deck.  
   - **No penalty** to the prize pool or payoff for doing so.

4. **Win Condition**  
   - After the Player’s *one* re‐spin (or no re‐spin), the Player’s 5‐card hand is compared to the Dealer’s 5‐card hand.  
   - If the Player’s final hand outranks the Dealer’s hand under standard poker rules, the Player wins **100% of the Prize Pool**; otherwise, payout is 0.

5. **Cost to Enter Bonus**  
   - We’ll call this cost **CostToEnterBonus**.


## 2. Determining the RTP (High‐Level)

```
RTP = (Expected Payout / Cost to Enter) × 100%

Where:
Expected Payout = Σ (Hand Probability × Prize Pool × Multiplier)
```

## 3. Model for the Player’s Strategy

#### Never Respin:
- Strong Hand Protection (`Never respin`):
   - Three of a kind
   - Three cards to royal flush
   - Three to straight flush
   - Three to flush
   - Three to straight

#### Conditional Respin:
- Pair Improvement:
   - With pair: Respin non-pair card
   - Exception: Don't respin if non-pair card is higher than dealer's visible cards

- Drawing Hands (Respin lowest non-contributing card):
   - Two to flush
   - Two to straight
   - Two to royal flush

- High Card Situations:
   - Respin lowest card unless:
     * It's higher than dealer's highest visible card
     * Lowest card > 10



## 4. Monte Carlo Simulatio
  
### 4.1 Simulation Process

1. Deck Setup
- Standard 52-card deck
- Shuffle before each deal


2. Deal Sequence
- Deal 3 face-up + 2 face-down to dealer
- Deal 3 face-up + 2 face-down to player
- Record visible cards


3. Decision Phase
- Evaluate player's hand
- Apply strategy matrix
- Execute respin if needed

4. Resolution
- Compare final hands
- Apply prize pool multiplier
-= Record outcome


## 5. Calculating the rtp

Bonus RTP Contribution = (Bonus Trigger Probability × Average Bonus Payout) / Cost to Enter Base Game