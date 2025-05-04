'''
File: Nuggets_Are_Great.py 

Name:Benjamin Hiller

Requirements:
Monte Carlo Simulation: Implement a Monte Carlo simulation to run multiple trials of the scenario.
Parameters: Use variables to store (and easily manipulate) the various parameters, such as:
Your 3-point percentage
Your 2-point percentage
Opponent's free-throw percentage
Time remaining in the game
Probability of offensive rebound
Probability of winning in overtime
Scenario Logic: Accurately represent the game logic, including:
Taking a 3-pointer and the potential outcomes (making it, missing it, winning in overtime)
Attempting to foul and the subsequent free-throws and potential offensive rebounds
Time management based on the score difference and time remaining
Output: Display the results of the simulation, including:
The percentage of wins for each strategy (taking a 3-pointer or fouling)
The average number of points scored in each scenario

Constants: 
SHOT_TIME_RANGES: Dictionary that stores time range in seconds for each shot type
POINTS: Dictionary that stores point values for each shot type

Variables: offensive_stats, defensive_stats, opponents_offensive_stats, opponents_defensive_stats, time_left, your_score, opponent_score, your_team_has_ball, in_overtime,
offensive_stats, defensive_stats, opponents_offensive_stats, opponents_defensive_stats, time_left, your_score, opponent_score, and your_team_has_ball

Inputs: Choice

calculated: 
Whether a shot is made based on probability
Who gets the rebound if a shot is missed
If the game goes to overtime
Final result (win or lose)

Output:
a little extra funny jib 
Win percentage for each strategy
Average points scored across all simulations


Key calculations: 
Random number checked against shooting percentages
Time is reduced based on actions like shots and rebounds
Final score is compared to decide the winner

Key design considerations: none

Test data: 
Running 1000 simulations as both the Nuggets and the Lakers shows realistic win/loss results based on NBA stats.
    When playing as the Nuggets:
        Three-pointer strategy resulted in 29.40% wins, avg points 122.1
        Fouling strategy resulted in 3.30% wins, avg points 117.7
    When playing as the Lakers:
        Three-pointer strategy resulted in 20.30% wins, avg points 121.0
        Fouling strategy resulted in 1.70% wins, avg points 117.1
This mirrors real-life tendencies: 3-pointers are risky but give a better chance at winning, and fouling late often fails against good free-throw shooters.
'''

import random

#Player stats
nuggets_player = {"The Joker":{"offense": {"two_pointer": 0.576, "three_pointer": 0.417, "free_throw": 0.80},"defense": {"rebound": 0.508}}}
lakers_player = {"The Crybaby":{"offense": {"two_pointer": 0.513, "three_pointer": 0.376, "free_throw": 0.782},"defense": {"rebound": 0.495}}}

#Time taken for each shot
shot_time_ranges = {"two-pointer": (5, 10),"three-pointer": (5, 10),"free-throw":(4, 8),}

#Amount of points for each shot
points = {"two-pointer": 2,"three-pointer": 3,"free-throw": 1,}

#Function for the whole game simulation
def game_simulation(offensive_stats, defensive_stats, opponents_offensive_stats, opponents_defensive_stats, shot_type, auto_foul):
    time_left = 30
    in_overtime = False
    your_team_has_ball = True
    your_score, opponent_score = 114, 117

    while True:
        #Regulation or overtime check
        if time_left <= 0:
            if not in_overtime and your_score == opponent_score:
                in_overtime = True
                time_left = 300
            else:
                break

        if your_team_has_ball:
            #Your teams shot attempt
            probability = offensive_stats[shot_type.replace("-", "_")]
            shot_time = random.randint(*shot_time_ranges[shot_type])
            time_left -= shot_time

            if random.random() < probability:
                your_score += points[shot_type]
                your_team_has_ball = False
            #Rebound    
            else:
                rebound_time = random.randint(1, 3)
                time_left -= rebound_time
                your_team_has_ball = random.random() < (1 - opponents_defensive_stats["rebound"])
        #Opponent possession                                               
        else:
            if auto_foul and time_left <= 30:
                #Fouling for loop
                for _ in range(2):
                    free_throw_time = random.randint(*shot_time_ranges["free-throw"])
                    time_left -= free_throw_time
                    if random.random() < opponents_offensive_stats["free_throw"]:
                        opponent_score += 1
                your_team_has_ball = True
            #Opponent normal shot
            else:
                opponents_shot = random.choice(["two-pointer", "three-pointer"])
                shot_time = random.randint(*shot_time_ranges[opponents_shot])
                time_left -= shot_time
                opponents_probability = opponents_offensive_stats[opponents_shot.replace("-", "_")]

                if random.random() < opponents_probability:
                    opponent_score += points[opponents_shot]
                    your_team_has_ball = True
                #Rebound
                else:
                    
                    rebound_time = random.randint(1, 3)
                    time_left -= rebound_time
                    your_team_has_ball = random.random() < defensive_stats["rebound"]

    you_win = your_score > opponent_score
    return you_win, your_score

def hardwood():
    print("\nWelcome to the hardwood!\n")
    #User input to choose team and strategy
    choice = ""
    while choice not in ["1", "2"]:
        choice = input("Enter 1 for Nuggets, 2 for Lakers: ")
        if choice == "1":
            offensive_stats = nuggets_player["The Joker"]["offense"]
            defensive_stats = nuggets_player["The Joker"]["defense"]
            opponents_offensive_stats = lakers_player["The Crybaby"]["offense"]
            opponents_defensive_stats = lakers_player["The Crybaby"]["defense"]
            print("\nIts hard to beat the refs!\n")
           
        elif choice == "2": 
            offensive_stats = lakers_player["The Crybaby"]["offense"]
            defensive_stats = lakers_player["The Crybaby"]["defense"]
            opponents_offensive_stats = nuggets_player["The Joker"]["offense"]
            opponents_defensive_stats = nuggets_player["The Joker"]["defense"]
            print("\nGross, the lakers. when was the last time they won a championship? Nevermind, no one cares!\n")
            
        else:
            print("\nThis aint football! You cant pick the Broncos!\n")
            
    simulations = int(input("Number of simulations: "))

    #Comparing the two strategies
    strategies = [("three-pointer strategy", "three-pointer", False), ("fouling strategy", "two-pointer", True),]

    for name, shot, auto_foul in strategies:
        wins = 0
        total_points = 0
        for _ in range(simulations):
            win, points = game_simulation(offensive_stats, defensive_stats, opponents_offensive_stats, opponents_defensive_stats, shot, auto_foul)
            wins += win
            total_points += points

        win_percentage = wins / simulations * 100
        average_points = total_points / simulations

        print(f"{name}: {win_percentage:.2f}% wins, avg points {average_points:.1f}")

if __name__ == "__main__":
    hardwood()

    
        