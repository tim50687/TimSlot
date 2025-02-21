import random 
from collections import defaultdict
import time


from card import Card, Suits, Deck
from hand_evaluation import Hand, HandRank
from strategy import RespinStrategy


class PokerBonusSimulator:
    def __init__(self, cost_to_enter: int = 1):
        self.cost_to_enter = cost_to_enter
        self.strategy = RespinStrategy()
        self.multipliers = {
            HandRank.ROYAL_FLUSH: 100000,
            HandRank.STRAIGHT_FLUSH: 10000,
            HandRank.FOUR_KIND: 1000,
            HandRank.FULL_HOUSE: 500,
            HandRank.FLUSH: 300,
            HandRank.STRAIGHT: 100,
            HandRank.THREE_KIND: 50,
            HandRank.TWO_PAIR: 25,
            HandRank.PAIR: 5,
            HandRank.HIGH_CARD: 3
        }

    def run_simulation(self, num_trials: int = 1000000):
        """Run Monte Carlo simulation and return results"""
        start_time = time.time()

        # money player win
        total_winnings = 0
        total_cost = num_trials * self.cost_to_enter
        # winning round
        wins = 0

        # Track statistics
        hand_frequencies = defaultdict(int)
        respin_stats = {"respun": 0, "not_respun": 0}
        winning_hands = defaultdict(int)

        for _ in range(num_trials):
            result = self.single_trial()
            total_winnings += result["payout"]

            if result["won"]:
                wins += 1
                winning_hands[result["player_hand"].rank] += 1
            
            hand_frequencies[result["player_hand"].rank] += 1

            if result["respun"]:
                respin_stats["respun"] += 1
            else:
                respin_stats["not_respun"] += 1

        # Calculate RTP of bonus round itself
        rtp = (total_winnings / total_cost) * 100
        
        elapsed_time = time.time() - start_time
        
        return {
            "trials": num_trials,
            "wins": wins,
            "win_rate": wins / num_trials * 100,
            "total_winnings": total_winnings,
            "total_cost": total_cost,
            "rtp": rtp,
            "avg_payout": total_winnings / num_trials,
            "hand_frequencies": {h.name: count / num_trials * 100 for h, count in hand_frequencies.items()},
            "winning_hands": {h.name: count / wins * 100 for h, count in winning_hands.items() if wins > 0},
            "respin_stats": respin_stats,
            "elapsed_time": elapsed_time
        }
    
    def single_trial(self):
        """Simulate a single bonus round and return the result"""
        deck = Deck()

        # Deal initial hands
        dealer_up = deck.deal(3)
        dealer_down = deck.deal(2)
        dealer_hand = dealer_up + dealer_down

        player_up = deck.deal(3)
        player_down = deck.deal(2)
        player_hand = player_up + player_down


        # Apply respin strategy
        card_to_respin = self.strategy.choose_respin(player_up, player_down, dealer_up)
        respun = False

        if card_to_respin is not None:
            respun = True
            player_hand.remove(card_to_respin)
            new_card = deck.deal(1)[0]
            player_hand.append(new_card)

        # Eval final hands
        final_player_hand = Hand(player_hand)
        final_dealer_hand = Hand(dealer_hand)

        # Compare hands and calculate payout
        player_wins = final_player_hand > final_dealer_hand
        payout = 0
        if player_wins:
            multiplier = self.multipliers[final_player_hand.rank]
            payout = self.cost_to_enter * multiplier

        
        return {
            "player_hand": final_player_hand,
            "dealer_hand": final_dealer_hand,
            "won": player_wins,
            "payout": payout,
            "respun": respun
        }
    
    def calculate_slot_rtp_contribution(self, results=None, num_trials: int = 1000000, 
                                   trigger_probability: float = 0.023324, base_bet: float = 1.0):
        """
        Calculate bonus round contribution to overall slot RTP
        
        Args:
            results: Existing simulation results (if None, will run a new simulation)
            num_trials: Number of simulation trials
            trigger_probability: Chance of entering bonus round (e.g., 0.023 = 2.3%)
            base_bet: Base bet in credits (typically 1.0)
            
        Returns:
            Bonus round's contribution to overall slot RTP
        """
        # Use existing results if provided, otherwise run a new simulation
        if results is None:
            results = self.run_simulation(num_trials)
        
        # Average payout from bonus round
        avg_bonus_payout = results['avg_payout']
        
        # Contribution to overall slot RTP
        bonus_rtp_contribution = (trigger_probability * avg_bonus_payout) / base_bet
        
        print(f"\n==== Bonus Round RTP Contribution ====")
        print(f"Bonus Trigger Probability: {trigger_probability:.4f} ({trigger_probability*100:.2f}%)")
        print(f"Average Bonus Payout: {avg_bonus_payout:.4f}x")
        print(f"Bonus RTP Contribution: {bonus_rtp_contribution:.4f} ({bonus_rtp_contribution*100:.2f}%)")
        print(f"(This represents {bonus_rtp_contribution:.2f}% of the total slot RTP)")
        
        return bonus_rtp_contribution
    
    def print_results(self, results):
        """Print formatted simulation results"""
        print(f"\n==== Poker Bonus Simulation Results ====")
        print(f"Trials: {results['trials']:,}")
        print(f"Time elapsed: {results['elapsed_time']:.2f} seconds")
        print(f"\nOutcomes:")
        print(f"  Wins: {results['wins']:,} ({results['win_rate']:.2f}%)")
        print(f"  RTP: {results['rtp']:.2f}%")
        print(f"  Average Payout: {results['avg_payout']:.4f}x")
        print(f"  Total Cost: {results['total_cost']:,}")
        print(f"  Total Winnings: {results['total_winnings']:,}")
        
        print(f"\nHand Frequencies:")
        for hand, freq in sorted(results['hand_frequencies'].items(), 
                                key=lambda x: HandRank[x[0]].value, reverse=True):
            print(f"  {hand}: {freq:.4f}%")
            
        print(f"\nWinning Hand Types:")
        for hand, freq in sorted(results['winning_hands'].items(), 
                                key=lambda x: HandRank[x[0]].value, reverse=True):
            print(f"  {hand}: {freq:.4f}%")
            
        print(f"\nRespin Statistics:")
        total = results['respin_stats']['respun'] + results['respin_stats']['not_respun']
        print(f"  Respun: {results['respin_stats']['respun']:,} ({results['respin_stats']['respun']/total*100:.2f}%)")
        print(f"  Not Respun: {results['respin_stats']['not_respun']:,} ({results['respin_stats']['not_respun']/total*100:.2f}%)")
        print("=======================================\n")



if __name__ == "__main__":
    # Example usage
    simulator = PokerBonusSimulator(1)
    
    # Run simulation once
    print("Running simulation...")
    results = simulator.run_simulation(num_trials=1000000)
    simulator.print_results(results)
    
    # Use the same results for RTP contribution calculation
    print("\nCalculating bonus round contribution to overall slot RTP...")
    simulator.calculate_slot_rtp_contribution(
        results=results, 
        trigger_probability=0.023,
        base_bet=1.0
    )