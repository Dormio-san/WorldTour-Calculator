# Planned features: 
# Let player select goal badge from drop down. Include number of points for that tier.
# Input box for current number of points.
# Display number of days remaining in the season. Season 8 ends December 11 2025
# Have points to next rank stat
# List number of daily points needed. Points needed / days left = daily points
# Include estimate for time to play as well as daily play time. 
# Also have input for player to put how long a match is. Maybe they want to add loading time to calculation.
# Potential additions: projected completion (based on time left and progress so far)
#   Estimated completion date (how many points  you've gotten per day so far, and use days left in season)

import tkinter as tk
import math
from datetime import date

# Points awarded for each round in world tour
lose_round_one_points = 2
lose_round_two_points = 6
lose_final_round_points = 14
win_final_round_points = 25

# Estimated time each game will take
game_time = 10

# Dates used to determine how much time is left in the season
season_end_date = date(2025, 12, 11)
today_date = date.today()


# Options in "Label: value" format
rank_options = [
    ("Bronze 4", 25),
    ("Bronze 3", 50),
    ("Bronze 2", 75),
    ("Bronze 1", 100),
    ("Silver 4", 150),
    ("Silver 3", 200),
    ("Silver 2", 250),
    ("Silver 1", 300),
    ("Gold 4", 375),
    ("Gold 3", 450),
    ("Gold 2", 525),
    ("Gold 1", 600),
    ("Platinum 4", 700),
    ("Platinum 3", 800),
    ("Platinum 2", 900),
    ("Platinum 1", 1000),
    ("Diamond 4", 1150),
    ("Diamond 3", 1300),
    ("Diamond 2", 1450),
    ("Diamond 1", 1600),
    ("Emerald 4", 1800),
    ("Emerald 3", 2000),
    ("Emerald 2", 2200),
    ("Emerald 1", 2400),
]

# Perform a division operation and round up the result
def division_round_up(dividend, divisor):
    return math.ceil(dividend / divisor)
    
def on_rank_selected(var_name, index, mode):
    # When user selects, update goal_points
    label, points = rank_dict[rank_var.get()]
    global goal_points
    goal_points = points
    goal_label.config(text=f"Goal points: {goal_points} ({label})")

def calculate():
    try:
        # The amount of points left to reach the goal points
        current_points = int(entry.get())
        points_remaining = goal_points - current_points
        
        # The number of games needed to reach the goal points
        # Includes losing first round, losing second round, losing final round, and winning final round
        round_one_games = division_round_up(points_remaining, lose_round_one_points)
        round_two_games = division_round_up(points_remaining, lose_round_two_points)
        lose_final_round_games = division_round_up(points_remaining, lose_final_round_points)
        win_final_round_games = division_round_up(points_remaining, win_final_round_points)
        
        # Estimated amount of play time to reach the goal points
        total_minutes = (points_remaining / 2) * game_time
        hours = int(total_minutes // 60)
        minutes = int(total_minutes % 60)
        days = hours // 24
        display = f"Points remaining: {points_remaining}\n"
        if days > 0:
            display += f"Estimated play time: {days} days, {hours%24} hours, {minutes} minutes\n"
        elif hours > 0:
            display += f"Estimated play time: {hours} hours, {minutes} minutes\n"
        else:
            display += f"Estimated play time: {minutes} minutes\n"
        
        # Estimated number of games required in each round to reach the goal points        
        display += f"Round one games: {round_one_games}\n"
        display += f"Round two games: {round_two_games}\n"
        display += f"Lose final round games: {lose_final_round_games}\n"
        display += f"Win final round games: {win_final_round_games}\n"
        
        # The amount of points needed per day to reach the goal points
        days_remaining = (season_end_date - today_date).days
        daily_points = points_remaining / days_remaining
        display += f"Days left in the season: {days_remaining}\n"
        display += f"Points needed per day: {daily_points}\n"
        
        result_label.config(text=display)
    except ValueError:
        result_label.config(text="Please enter a valid number.")

root = tk.Tk()
root.title("World Tour Points Calculator")

rank_dict = {f"{label}: {points}": (label, points) for label, points in rank_options}
dropdown_options = list(rank_dict.keys())

rank_var = tk.StringVar()
rank_var.set(dropdown_options[-1])  # Default to Emerald 1: 2400

goal_points = rank_dict[rank_var.get()][1]

rank_menu = tk.OptionMenu(root, rank_var, *dropdown_options)
rank_menu.pack(pady=8)

# Whenever rank_var is changed, on_rank_selected will run
rank_var.trace_add("write", on_rank_selected)

goal_label = tk.Label(root, text=f"Goal points: {goal_points}")
goal_label.pack(pady=8)

# Update the goal label text when the game first runs
on_rank_selected("name", 1, "mode")

tk.Label(root, text="Enter current points:").pack(pady=5)
entry = tk.Entry(root)
entry.pack(pady=5)

calc_button = tk.Button(root, text="Calculate", command=calculate)
calc_button.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=30)

root.geometry("500x450")
root.mainloop()
