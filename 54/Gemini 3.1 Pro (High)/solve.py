def evaluate(hand):
    values_dict = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
    values = sorted([values_dict[card[0]] for card in hand], reverse=True)
    suits = [card[1] for card in hand]
    
    is_flush = len(set(suits)) == 1
    
    is_straight = False
    if len(set(values)) == 5 and values[0] - values[4] == 4:
        is_straight = True

    from collections import Counter
    counts = Counter(values)
    sorted_freqs = sorted([(freq, val) for val, freq in counts.items()], reverse=True)
    
    freq_pattern = tuple(f for f, v in sorted_freqs)
    ordered_vals = [v for f, v in sorted_freqs]
    
    if is_flush and is_straight:
        if ordered_vals[0] == 14:
            return (9, ordered_vals) # Royal Flush
        return (8, ordered_vals) # Straight Flush
    
    if freq_pattern == (4, 1):
        return (7, ordered_vals) # Four of a kind
    
    if freq_pattern == (3, 2):
        return (6, ordered_vals) # Full house
        
    if is_flush:
        return (5, ordered_vals) # Flush
        
    if is_straight:
        return (4, ordered_vals) # Straight
        
    if freq_pattern == (3, 1, 1):
        return (3, ordered_vals) # Three of a kind
        
    if freq_pattern == (2, 2, 1):
        return (2, ordered_vals) # Two pairs
        
    if freq_pattern == (2, 1, 1, 1):
        return (1, ordered_vals) # One pair
        
    return (0, ordered_vals) # High card

p1_wins = 0
import os

filepath = os.path.join(os.path.dirname(__file__), '..', 'poker.txt')

with open(filepath, 'r') as f:
    for line in f:
        cards = line.strip().split()
        if not cards: continue
        h1 = cards[:5]
        h2 = cards[5:]
        if evaluate(h1) > evaluate(h2):
            p1_wins += 1

print(p1_wins)
