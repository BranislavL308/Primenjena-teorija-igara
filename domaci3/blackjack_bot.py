# %%
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.histograms import _unsigned_subtract

#def player and dealer
# define global variables

global player_state_value 
player_state_value = {}

global player_states
player_states = []

global player_win 
player_win = 0

global player_draw
player_draw = 0


def give_card():
    card_list = list(range(1, 11)) + [10, 10, 10]
    return np.random.choice(card_list)

#cards = give_card()
#print(cards)


def dealer_policy(current_val, usable_ace, is_end):
    if current_val > 21:
        if usable_ace:
            current_val -= 10
            usable_ace = False
        else:
            return current_val, usable_ace, True

    if current_val >= 17:
        return current_val, usable_ace, True
    else:
        card = give_card()
        if card == 1:
            if current_val <=10:
                return current_val + 11, True, False
            return current_val + 1, usable_ace, False
        else:
            return current_val + card, usable_ace, False


def player_policy(current_val, usable_ace, is_end):
    if current_val > 21:
        if usable_ace:
            current_val -= 10
            usable_ace = False
        else:
            return current_val, usable_ace, True

    if current_val >= 20:
        return current_val, usable_ace, True
    else:
        card = give_card()
        if card == 1:
            if current_val <=10:
                return current_val + 11, True, False
            return current_val + card, usable_ace, False
        else:
            return current_val + card, usable_ace, False

def give_reward(player_value, dealer_value, is_end = True):
    if is_end:
        last_state = player_states[-1]
        if player_value > 21:
            if dealer_value > 21:
                #draw
                global player_draw
                player_draw +=1
            else:
                player_state_value[last_state] -=1
        else:
            if dealer_value > 21:
                player_state_value[last_state] += 1
                global player_win
                player_win +=1
            else:
                if player_value  < dealer_value :
                    player_state_value[last_state] -= 1
                elif player_value > dealer_value:
                    player_state_value[last_state] +=1;
                    player_win +=1
                else:
                    player_draw +=1

def play_game(rounds = 1000):
    for i in range(rounds):
        if i % 1000 == 0:
            print("round", i)
        # hit 2 cards each
        dealer_value = 0 
        player_value = 0
        show_card = 0
        dealer_value += give_card()
        show_card = dealer_value
        dealer_value += give_card()

        #player's turn
        # alway hit if less than 12

        usable_ace = False
        is_end = False

        while True:
            player_value, usable_ace, is_end = player_policy(player_value, usable_ace, is_end)

            if is_end:
                break

            if (player_value >= 10) and (player_value <=21):
                player_states.append((player_value, show_card, usable_ace))

        usable_ace, is_end = False, False

        while not is_end:
            dealer_value, usable_ace, is_end = dealer_policy(dealer_value, usable_ace, is_end)

        for s in player_states:
            player_state_value[s] = 0 if player_state_value.get(
                s) is None else player_state_value.get(s)

        give_reward(player_value, dealer_value)
        print(player_value)


# %%
def train():
    rounds = 10000
    play_game(rounds)

    print("Player wining rate", player_win / rounds)
    print("Not losing rate", (player_win + player_draw) / rounds)




# %%
train()

# %%
