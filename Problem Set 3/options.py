# This file contains the options that you should modify to solve Question 2

# IMPORTANT NOTE:
# Comment your code explaining why you chose the values you chose.
# Uncommented code will be penalized.

def question2_1():
    #TODO: Choose options that would lead to the desired results 
    return {
        "noise": 0, # Actions taken near to deterministic behavior important as it's dangerous path --> we need low noise
        "discount_factor": 0.5, # Future rewards are considered important.
        "living_reward": -1 # to seek the near terminal
    }

def question2_2():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.3, # Increase noise to make safe path selection more likely
        "discount_factor": 0.6, # Future rewards are considered important.
        "living_reward": -1 # to seek the near terminal
    }

def question2_3():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0, # Actions taken near to deterministic behavior important as it's dangerous path --> we need low noise
        "discount_factor": 0.8,  # To highly priortize future rewards 
        "living_reward": -0.1 # to seek the far terminal state
    }

def question2_4():
    #TODO: Choose options that would lead to the desired results
        return {
        "noise": 0.1, # Increase noise to make safe path selection more likely
        "discount_factor": 1,  # To highly priortize future rewards 
        "living_reward": -0.1  # to seek the far terminal state
    }

def question2_5():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0, 
        "discount_factor": 1,
        "living_reward": 1 # Keep getting rewards -> life is so good so taking long time maybe forever
    }

def question2_6():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": -100 # Tries to end his life as life is so bad (getting penalized very high)
    }