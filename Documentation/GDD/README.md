# Tim Slot - Game Design Document

## 1. Project Overview
### 1.1. Game Summary
- A slot machine game that combines traditional slot mechanics with poker-based bonus round.
- Target platform: PC
- Target audience: slot lovers, poker lovers

### 1.2 Core Features
- Classic 3x3 slot machine layout
- Poker-based bonus round featuring player decisions
- Mathematical model that ensures casino profitability
- Engaging animations and sound effects (do my best)

## 2. Game Mechanics

### 2.1 Base Game
#### 2.1.1 Slot Layout
- 3x3 grid layout
- 5 paylines:
    - Middle row


#### 2.1.2 Symbols
- Ace, King, Queen, Jack, 10, 9, 8, 7, 6, 5, 4, 3, 2
- Bonus symbol

#### 2.1.3 Paytable
Symbol Combinations (Left to Right)

3 of a Kind Payouts (Multiplier of Bet):

- Ace    - 100x
- King   - 75x
- Queen  - 50x
- Jack   - 25x
- 10     - 15x
- 9      - 12x
- 8      - 10x
- 7      - 8x
- 6      - 6x
- 5      - 5x
- 4      - 4x
- 3      - 3x
- 2      - 2x



### 2.2 Bonus Round

#### 2.2.1 Triggering the Bonus Round
- Three bonus symbols on
    - Middle row



#### 2.2.2 Bonus Round Mechanics

Initial steps:
- Dealer deals 5 cards (3 face up, 2 face down)
- Player deals 5 cards (3 face up, 2 face down)
- Prize Pool displayed

Gameplay:
- Player can choose any face up card to replace 1 time


#### 2.2.3 Winning Conditions
You have to beat the dealer's hand to win the prize pool.

- Royal Flush: 10x prize pool (Odds: 0.000154%)
- Straight Flush: 5x prize pool (Odds: 0.00139%)
- Four of a Kind: 4x prize pool (Odds: 0.0240%)
- Full House: 3.5x prize pool (Odds: 0.1441%)
- Flush: 3x prize pool (Odds: 0.1965%)
- Straight: 2x prize pool (Odds: 0.3925%)
- Three of a Kind: 1.5x prize pool (Odds: 2.1128%)
- Two Pair: 1.2x prize pool (Odds: 4.7539%)
- Pair: 1x prize pool (Odds: 42.2569%)
- High Card: 5x prize pool (Odds: 50.1177%)


## 3. Visual and Audio Design

### 3.1 Visual Style
- Clean interface
- Clear symbol
- Effects for wins
- Dynamic lighting for bonus rounds
- Effects for bonus round win

### 3.2 Audio Design
- Background music
- Reel spinning sounds
- Win celebration sounds
- Bonus round entry music
- Card dealing sounds
- Bonus round win sounds

## 4. User Interface

### 4.1 Main game screen
- Credit display
- Bet display
- Spin button
- Paytable button
- Win display
- Payline display

### 4.2 Bonus round screen
- Player's cards
- Dealer's cards
- Prize pool display
- Respin button
- Timer display

## 5. Mathematics

### 6.1 Base Game
- Target RTP: 88-92%
- Hit frequency: ~20%
- Maximum win: 100x bet

### 6.2 Bonus Game
- Trigger frequency: ~1%
- Average bonus value: 50x bet
- Maximum bonus win: 500x bet