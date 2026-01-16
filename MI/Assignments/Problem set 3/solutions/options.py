# This file contains the options that you should modify to solve Question 2

# IMPORTANT NOTE:
# Comment your code explaining why you chose the values you chose.
# Uncommented code will be heavily penalized.


def question2_1():
    # Short dangerous path, reach +1 quickly.
    # No noise → deterministic short path.
    # Very small discount → agent values immediate reward.
    # Negative living reward → encourages fast termination.
    return {
        "noise": 0.0,
        "discount_factor": 0.05,
        "living_reward": -1.0
    }


def question2_2():
    # Short near reward but prefer long **safe** path.
    # Some noise so agent avoids the risky -10 zone.
    # Low discount → near terminal still attractive.
    # Mild negative reward encourages movement but avoids danger.
    return {
        "noise": 0.15,
        "discount_factor": 0.3,
        "living_reward": -0.5
    }


def question2_3():
    # Prefer far +10 terminal using the short dangerous path.
    # No noise → shortest risky path is viable.
    # High discount → future +10 is valuable.
    # Negative living reward → encourages quick termination.
    return {
        "noise": 0.0,
        "discount_factor": 1.0,
        "living_reward": -1.0
    }


def question2_4():
    # Prefer far +10 terminal but using the **safe** long path.
    # Some noise → avoids the dangerous row.
    # High discount → heavily values future +10.
    # Slight negative reward → motivates reaching terminal efficiently.
    return {
        "noise": 0.25,
        "discount_factor": 1.0,
        "living_reward": -0.05
    }


def question2_5():
    # Avoid ALL terminal states forever.
    # No noise necessary.
    # High discount → future is important.
    # Positive living reward → staying alive forever is best.
    return {
        "noise": 0.0,
        "discount_factor": 1.0,
        "living_reward": 2.0
    }


def question2_6():
    # I want the policy to seek any terminal state (even ones with the -10 penalty) 
    # and try to end the episode in the shortest time possible
    # no noise needed as the agent moves exactly as intended
    # high discount factor (1) ensures the agent values the terminal state, even with a penalty
    # very high negative living reward (-20) forces the agent to reach a terminal state as quickly as possible, even if it means enduring penalties
    return {
        "noise": 0.0,
        "discount_factor": 1.0,
        "living_reward": -25.0
    }
